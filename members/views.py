import json
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import UserSignUpForm, ProfileSignUpForm, CreateListingForm, EditListingForm, UserEditForm, UserPasswordChangeForm, ScoreForm
from django.contrib import messages
from items.models import Item, ItemCondition, Sport
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Profile, Score
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models import Q

# Create your views here.
def get_header_images():
    image_folder = os.path.join(settings.MEDIA_ROOT, 'header_images')
    image_urls = [
        f"{settings.MEDIA_URL}header_images/{image}" for image in os.listdir(image_folder)
    ]
    return image_urls

def login_user(request):
    if request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username = username, password = password)
        if user:
            login(user=user, request=request)
            messages.success(request, ("You have successfully logged in!"))
            return redirect("home")
        else:
            messages.success(request, ("Login failed, please try again!"))
            return redirect("login")
    else:
        return render(request, 'login.html')
    
def about(request):
    image_urls = get_header_images()

    return render(request, 'about.html', {
        'images': json.dumps(image_urls)
    })

def home(request):
    #return render(request, 'home.html', {})

    sports = Sport.objects.all()
    conditions = ItemCondition.objects.all()


    selected_conditions = request.GET.getlist('conditions')
    selected_sports = request.GET.getlist('sports')
    search_query = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    items = Item.objects.filter(sold = False)
    
    if request.user.is_authenticated:
        items = items.exclude(advertiser=request.user.profile)

    if search_query:
        items = items.filter(name__icontains=search_query)

    
    if selected_sports:
        items = items.filter(sport__id__in=selected_sports)
   
    if selected_conditions:
        items = items.filter(condition__id__in=selected_conditions)

    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)


    sort_option = request.GET.get('sort')

    if sort_option == 'name_asc':
        items = items.order_by('name')
    elif sort_option == 'name_desc':
        items = items.order_by('-name')
    elif sort_option == 'price_asc':
        items = items.order_by('price')
    elif sort_option == 'price_desc':
        items = items.order_by('-price')

    paginator = Paginator(items, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    image_urls = get_header_images()

    return render(request, 'home.html', {
        'page_obj': page_obj,
        #'items': items,
        'sports': sports,
        'conditions': conditions,
        'selected_sports': selected_sports,
        'selected_conditions': selected_conditions,
        'sort_option': sort_option,
        'min_price': min_price,
        'max_price': max_price,
        'images': json.dumps(image_urls)
    })

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out!"))
    return redirect("home")

def signup_user(request):
    if request.method == 'POST':
        userform = UserSignUpForm(request.POST)
        profileform = ProfileSignUpForm(request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, 'You have successfully registered!')
            return redirect("home")
        else:
            messages.error(request, 'An error happened!')
    userform = UserSignUpForm()
    profileform = ProfileSignUpForm()
    return render(request, "signup.html", {"userform": userform, "profileform": profileform })

def item(request, pk):
    current_item = get_object_or_404(Item, id=pk)
    
    items = Item.objects.exclude(id=current_item.id)
    related_items = items.filter(sold = False, sport=current_item.sport)

    return render(request, 'item.html', {
        'item': current_item,
        'related_items': related_items,
        #'userpk': current_item.profile.user.pk
    })

@login_required(login_url="/members/login/")
def createlisting(request):
    if request.method == 'POST':
        itemform = CreateListingForm(request.POST, request.FILES)
        if itemform.is_valid(): 
            item = itemform.save(commit = False)
            item.advertiser = request.user.profile
            item.save()
            messages.success(request, 'You have successfully uploaded a new item!')
            return redirect("my_ads")
        else:
            messages.error(request, 'Error happened while you were uploading a new item!')
            print(itemform.errors)
    listingform = CreateListingForm()
    return render(request, "additem.html", {"listingform": listingform})

@login_required(login_url="/members/login/")
def my_ads(request):
    user_profile = request.user.profile
    user_items = Item.objects.filter(advertiser=user_profile)

    if request.method == "POST":
        item_ids = request.POST.getlist('item_ids')
        if item_ids:
            Item.objects.filter(id__in=item_ids, advertiser=user_profile).delete()
            messages.success(request, "Selected items were deleted successfully.")
        return redirect('my_ads')

    return render(request, 'my_ads.html', {'user_items': user_items})
    
@login_required(login_url="/members/login/")
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = EditListingForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_ads')
    form = EditListingForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required(login_url="/members/login/")
def my_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileSignUpForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('my_profile')
        else:
            messages.error(request, "An error occurred. Please try again.")
            print(user_form.errors, profile_form.errors)
    
    user_form = UserEditForm(instance=user)
    profile_form = ProfileSignUpForm(instance=profile)

    return render(request, 'my_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required(login_url="/members/login/")
def change_password(request):
    if request.method == 'POST':
        passwordform  = UserPasswordChangeForm(user=request.user, data=request.POST)
        if passwordform.is_valid():
            passwordform.save()
            update_session_auth_hash(request, request.user)
            return redirect('my_profile')
        else:
            messages.error(request, passwordform.error_messages)
            return redirect('change_password')
    else:
        return render(request, 'change_password.html', {'form': UserPasswordChangeForm(request.user)})

def advertisers(request):
    search_query = request.GET.get('search', '').strip()
    sort_option = request.GET.get('sort')
    page = request.GET.get('page', 1) 
    
    advertisers = Profile.objects.annotate(average_score=Avg('user__received_scores__score'))

    if search_query:
        advertisers = advertisers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    if sort_option == 'name_asc':
        advertisers = advertisers.order_by('user__first_name')
    elif sort_option == 'name_desc':
        advertisers = advertisers.order_by('-user__first_name')
    elif sort_option == 'score_asc':
        advertisers = advertisers.order_by('average_score')
    elif sort_option == 'score_desc':
        advertisers = advertisers.order_by('-average_score')

    paginator = Paginator(advertisers, 10) 
    try:
        advertisers = paginator.page(page)
    except PageNotAnInteger:
        advertisers = paginator.page(1)
    except EmptyPage:
        advertisers = paginator.page(paginator.num_pages)

    user_scores = {}
    if request.user.is_authenticated:
        for advertiser in advertisers:
            try:
                score = Score.objects.get(rater_user=request.user, rated_user=advertiser.user)
                user_scores[advertiser.user.id] = score
            except Score.DoesNotExist:
                user_scores[advertiser.user.id] = None

    form = ScoreForm()
    return render(request, 'advertisers.html', {
        'advertisers': advertisers,
        'form': form,
        'sort_option': sort_option,
        'user_scores': user_scores,
        'images': json.dumps(get_header_images())
    })

@login_required
def add_score(request, user_id):
    rated_user = get_object_or_404(User, id=user_id)
    if rated_user == request.user:
        return redirect('advertisers')  
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score, created = Score.objects.update_or_create(
                rater_user=request.user,
                rated_user=rated_user,
                defaults={'score': form.cleaned_data['score']}
            )
            messages.success(request, "Score updated successfully!" if not created else "Score added successfully!")
            return redirect('advertisers')
    else:
        form = ScoreForm()

    return render(request, 'add_score.html', {'form': form, 'rated_user': rated_user})