# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from .forms import UserCreationForm, PropertyForm
from django.contrib.auth.decorators import login_required
from .models import Property, Listing, Booking

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')
        else:
            # If form is not valid, re-render the registration form with errors
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'seller':
                return redirect('seller_dashboard')
            elif user.role == 'buyer':
                return redirect('listing_view')  # Adjust this to your actual URL name for the buyer's listings page
            else:
                return redirect('home')  # Redirect to some default page if role is unknown
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


@login_required
def seller_dashboard(request):
    if request.user.role != 'seller':
        return HttpResponse("You are not authorized to view this page.")

    # Exclude listings that are already booked
    booked_listings = Booking.objects.values_list('listing_id', flat=True)
    listings = Listing.objects.exclude(listing_id__in=booked_listings)

    form = PropertyForm()  # Move this line outside of the POST condition

    return render(request, 'seller_dashboard.html', {'listings': listings, 'form': form})


def seller_logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def listing_view(request):
    if request.user.role != 'buyer':
        return HttpResponse("You are not authorized to view this page.")

    # Exclude listings that are already booked
    booked_listings = Booking.objects.values_list('listing_id', flat=True)
    listings = Listing.objects.exclude(listing_id__in=booked_listings)

    return render(request, 'listing_view.html', {'listings': listings})

def buyer_logout(request):
    auth_logout(request)
    return redirect('login')


def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            bedrooms = form.cleaned_data['bedrooms']
            bathrooms = form.cleaned_data['bathrooms']
            sqft = form.cleaned_data['sqft']
            ptype = form.cleaned_data['ptype']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']

            # Create a new property object
            property_obj = Property.objects.create(name=name, address=address, bedrooms=bedrooms,
                                                    bathrooms=bathrooms, sqft=sqft, ptype=ptype)

            # Create a new listing object associated with the property
            listing_obj = Listing.objects.create(property=property_obj, user=request.user,
                                                  name=name, price=price, description=description)

            # Redirect to the seller dashboard
            return redirect('seller_dashboard')
    else:
        form = PropertyForm()

    return render(request, 'seller_dashboard.html', {'form': form})