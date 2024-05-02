# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from .forms import UserCreationForm, PropertyForm
from django.contrib.auth.decorators import login_required
from .models import Property, Listing, Booking, Review, Booking


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

    # Filter listings by the current logged-in user
    listings = Listing.objects.filter(user=request.user)

    # Get all bookings for each listing
    bookings_per_listing = {}
    for listing in listings:
        bookings = Booking.objects.filter(listing=listing)
        bookings_per_listing[listing] = bookings

    return render(request, 'seller_dashboard.html', {'listings': listings, 'bookings_per_listing': bookings_per_listing})

def seller_logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def listing_view(request):
    if request.user.role != 'buyer':
        return HttpResponse("You are not authorized to view this page.")

    # Get all listings that are not booked
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


def property_details(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    listing = property_obj.listings.first()  # Assuming one listing per property for simplicity
    reviews = Review.objects.filter(listing=listing)  # Get reviews for this listing

    # Pass property, listing, and reviews to the template
    return render(request, 'property_details.html', {'property': property_obj, 'listing': listing, 'reviews': reviews})

def delete_listing(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        property_id = listing.property_id
        listing.delete()

        # Also delete the associated property
        Property.objects.filter(property_id=property_id).delete()

    return redirect('seller_dashboard')

def add_comment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        comment = request.POST['comment']
        # Create a new review object with the comment
        review = Review.objects.create(listing=listing, user=request.user, comment=comment)
        # Redirect back to the property details page
        return redirect('property_details', property_id=listing.property_id)
    else:
        # If the request method is not POST, redirect to some other page
        return redirect('home')  # Adjust this to your desired URL

def book_property(request, listing_id):
    if request.method == 'POST':
        # Assuming you have a form to handle the booking process
        # Extract the listing and user information from the request
        listing = Listing.objects.get(pk=listing_id)
        user = request.user

        # Create a new booking entry
        booking = Booking.objects.create(listing=listing, user=user)

        # Optionally, you can add more logic here such as sending a confirmation email

        return redirect('property_details', property_id=listing.property_id)

    # If the request method is not POST, you may handle it differently, such as showing an error page
    return redirect('property_details', property_id=listing.property_id)
