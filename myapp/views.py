from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from operator import itemgetter
from django.utils import timezone
from .models import Items, Outfits, UserProfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
import requests, base64
from bs4 import BeautifulSoup
from io import BytesIO

def sign_out(request):
    logout(request)
    # Redirect the user to a page indicating successful sign out or to the home page
    return redirect('/home/')

colorList=["blue","cyan","white","navy blue","green","black","grey","red","pink","brown","beige","yellow","maroon","olive","orange","purple","peach","cream","teal","mustard","multi","burgandy","charcoal","lavender","coral","magenta","lime green","silver","gold","metalic"]

colorValue=[8,7,8.5,8,7,8.5,7,8,6,6,7.5,7.5,8,8,8,8,7.5,7.5,7,7,8,7.8,8,8,6,7.5,8,7,7,7]
def home(request):

    # isActive = False
    # if request.method == 'POST':
    #     check = request.POST.get('check')
    #     print(check)
    #     if check is None: isActive=False
    #     else:   isActive=True
    # name = 'Darshan'
    # date = str(datetime.datetime.now())

    # student = {
    #     "name": "Darshan",
    #     "age" : 21,
    #     "gender": "M"
    # }
    # list_of_programs = ['WAP to check even or odd',
    #     'WAP to check prime number',
    #     'WAP to print all prime numbers from 1 to 100',
    #     'WAP to print pascals triangle']
    # data = {
    #     'date': date,
    #     'isActive': isActive,
    #     'name': name,
    #     'list_of_programs': list_of_programs,
    #     'student': student
    # }
    return render(request, "home.html", {})

def mixnmatch(request):
    html = "<h1>MixnMatch</h1>"
    # return HttpResponse(html)
    return render(request, "mixnmatch.html", {})

def about(request):
    return render(request, "about.html", {})

def closet(request):
    # return HttpResponse("Closet page")
    if request.user.is_authenticated:
        items = Items.objects.filter(user=request.user)
    else:
        items=[]
    return render(request, "closet.html", {'items':items})

def add_item(request):
    if request.method=='POST' and request.user.is_authenticated:
        #fetch kar rahe data ko idhar
        user_instance=request.user
        item_name = request.POST.get("item_name")
        item_category = request.POST.get("item_category")
        item_color = request.POST.get("item_color")
        item_brand = request.POST.get("item_brand")
        item_price = float(request.POST.get("item_price"))
        item_type = request.POST.get("item_type")
        # item_photo = request.POST.get("item_photo")
        item_photo=request.FILES.get('item_photo')
        if item_category == "Topwear":
            item_pattern = request.POST.get("item_pattern")
        else:
            item_pattern = "Null"
        # print(item_photo)

        #model ka object bana rahe idhar
        item = Items(Items.objects.create(
            user=user_instance,
            name=item_name,
            category=item_category,
            pattern=item_pattern,
            color=item_color,
            brand=item_brand,
            price=item_price,
            type=item_type,
            photo=item_photo,
            time=timezone.now()
        ))
        u=UserProfile.objects.get(user=user_instance)
        u.item_time=timezone.now()
        u.save()
        return redirect("/closet/")
    else: []
    return render(request, 'add_item.html', {})

def calculate_score(request, upper, lower, bottom):
    List=["blue","cyan","white","navy blue","green","black","grey","red","pink","brown","beige","yellow","maroon","olive","orange","purple","peach","cream","teal","mustard","multi","burgandy","charcoal","lavender","coral","magenta","lime green","silver","gold","metalic"]
    user_data=UserProfile.objects.get(user=request.user)
    upper_color=user_data.upper_fav_colors
    lower_color=user_data.lower_fav_colors
    bottom_color=[8,7,8.5,8.5,7,8.5,7,7,7,7.5,7.5,7.5,7.5,7,7.6,7.7,7,7.5,7,6,8,7.6,8,7.6,6,7.5,8,7,7,7]
    if(upper.type ==lower.type ==bottom.type ):
        color_score = upper_color[List.index(upper.color)] + lower_color[List.index(lower.color)] + bottom_color[List.index(bottom.color)]
    elif(upper.type ==lower.type =="Formal" and (bottom.type =="Casual" or bottom.type =="Ocassional")):
        color_score = upper_color[List.index(upper.color)] + lower_color[List.index(lower.color)] + lower_color[List.index(lower.color)]* 0.5
    elif(upper.type =="Formal" and lower.type =="Casual" and (bottom.type =="Casual" or bottom.type =="Formal")):
        color_score = upper_color[List.index(upper.color)] + lower_color[List.index(lower.color)]* 0.6+ lower_color[List.index(lower.color)]
    elif(upper.type =="Ocassional" and lower.type =="Formal" and (bottom.type =="Ocassional" or bottom.type =="Formal")):
        color_score = upper_color[List.index(upper.color)] + lower_color[List.index(lower.color)]* 0.5+ lower_color[List.index(lower.color)]

    else:
        return 0

    total_score = color_score
    
    return total_score

def calc_type(upr,lowr,botm):
    if(upr==lowr==botm):
        return upr
    elif(upr=="Formal" and lowr=="Casual" and (botm=="Casual" or botm=="Formal")):
        return "Semi-Formal"
    else:
        return upr

def make_outfits(request):
    if request.user.is_authenticated:
        user_id=request.user
        #  and (lower.user==upper.user),and (bottom.user==lower.user)
        items = Items.objects.filter(user=user_id)
        outfits = []
        for upper in items:
            if upper.category == 'Topwear':
                for lower in items:
                    if lower.category == 'Bottomwear':
                        for bottom in items :
                            if bottom.category == 'Footwear':
                                outfit = Outfits()
                                if not Outfits.objects.filter(Q(upper_id=upper.id) & Q(lower_id=lower.id) & Q(foot_id=bottom.id)).exists():
                                    outfit.user=user_id
                                    outfit.upper_id=upper.id
                                    outfit.lower_id=lower.id
                                    outfit.foot_id=bottom.id
                                    outfit.type = calc_type(upper.type, lower.type, bottom.type)
                                    outfit.score = calculate_score(request,upper, lower, bottom)
                                    outfit.save()
                                    
        otfts=Outfits.objects.filter(user=request.user)
        for o in otfts:
            upper = Items.objects.get(id=o.upper_id)
            lower = Items.objects.get(id=o.lower_id)
            foot = Items.objects.get(id=o.foot_id)
            outfits.append({
                'id': o.id,
                'upper_path': upper.photo.url,
                'lower_path': lower.photo.url,
                'bottom_path': foot.photo.url,
                'type': o.type,
                'score': o.score,
                'like':o.like
            })
        sorted_outfits = sorted(outfits, key=lambda outfit: outfit['score'], reverse=True)
    else: sorted_outfits=[]
    u=UserProfile.objects.get(user=request.user)
    u.outfit_time=u.item_time
    u.save()                                                 
    return sorted_outfits


def outfits(request):
    u=UserProfile.objects.get(user=request.user)
    outfits=[]
    print(u.outfit_time)
    if(u.outfit_time == None):
        outfits = make_outfits(request)
        u.outfit_time=u.item_time
    elif(u.item_time>u.outfit_time):  
        outfits = make_outfits(request)
        u.outfit_time=u.item_time      
    else:
        otfts=Outfits.objects.filter(user=request.user)
        for o in otfts:
            upper = Items.objects.get(id=o.upper_id)
            lower = Items.objects.get(id=o.lower_id)
            foot = Items.objects.get(id=o.foot_id)
            outfits.append({
                'id': o.id,
                'upper_path': upper.photo.url,
                'lower_path': lower.photo.url,
                'bottom_path': foot.photo.url,
                'type': o.type,
                'score': o.score,
                'like' :o.like
            })
        outfits = sorted(outfits, key=lambda outfit: outfit['score'], reverse=True)
    u.save()
    dict={'outf':[],'recom':[]}
    dict["outf"]=outfits
    dict["recom"]=outfit_recommendations(request, request.user)
    

    return render(request, 'outfits.html', {'outfits': dict})

def outfit_recommendations(request, user_id):
    List=["blue","cyan","white","navy blue","green","black","grey","red","pink","brown","beige","yellow","maroon","olive","orange","purple","peach","cream","teal","mustard","multi","burgandy","charcoal","lavender","coral","magenta","lime green","silver","gold","metalic"]
    typelist=["Formal","Semi-Formal","Casual","Ocassional","Festive Wear"]
    user_vectors = Outfits.objects.filter(user=user_id, like=True).values('id', 'upper_id', 'lower_id', 'foot_id', 'type')
    for outfit in user_vectors:
    # Fetch upper color
        upper_item_id = outfit['upper_id']
        outfit['upper_id'] = List.index(Items.objects.get(id=upper_item_id).color)+1
        lower_item_id = outfit['lower_id']
        foot_item_id = outfit['foot_id']
        outfit['lower_id'] = List.index(Items.objects.get(id=lower_item_id).color)+1
        outfit['foot_id'] = List.index(Items.objects.get(id=foot_item_id).color)+1
        outfit['type'] = typelist.index(outfit['type'])+1
    
    user_vector_array = np.array([list(item.values())[1:] for item in user_vectors])

    # Normalize the vectors
    normalized_user_vector = user_vector_array / np.linalg.norm(user_vector_array, axis=1)[:, np.newaxis]


    # Step 3: Calculate User Similarities
    all_user_vectors = (
        Outfits.objects.filter(like=True)
        .exclude(user=user_id)
        .values('id', 'user', 'upper_id', 'lower_id', 'foot_id', 'type')
    )
    for u in all_user_vectors:
        upper_item_id=u['upper_id']
        lower_item_id = u['lower_id']
        foot_item_id = u['foot_id']
        u['upper_id']=List.index(Items.objects.get(id=upper_item_id).color)+1
        u['lower_id']=List.index(Items.objects.get(id=lower_item_id).color)+1
        u['foot_id']=List.index(Items.objects.get(id=foot_item_id).color)+1
        u['type'] = typelist.index(u['type'])+1

    all_user_vector_array = np.array([list(item.values())[2:] for item in all_user_vectors])
    normalized_all_user_vectors = all_user_vector_array / np.linalg.norm(all_user_vector_array, axis=1)[:, np.newaxis]

    # Calculate cosine similarities
    similarities = cosine_similarity(normalized_user_vector, normalized_all_user_vectors)[0]
    threshold = similarities.mean()

    # Step 4: Identify Similar Users
    similar_users = {item['user'] for item, similarity in zip(all_user_vectors, similarities) if similarity >= threshold}
    print(similar_users)
    # Step 5: Generate Outfit Recommendations
    user_outfits = Outfits.objects.filter(user=user_id,like=True).values_list('id', flat=True)
    recommended_outfits = []

    for similar_user_id in similar_users:
        similar_user_outfits= Outfits.objects.filter(user=similar_user_id,like=True).values_list('id', flat=True)
        print(similar_user_outfits)
        for o in similar_user_outfits:
            recommended_outfits.append(o)
    # Fetch recommended outfits details
    # recommended_outfit_details = Outfits.objects.filter(id=recommended_outfits)
    recom=[]
    for i in recommended_outfits:
        o=Outfits.objects.get(id=i)
        upper = Items.objects.get(id=o.upper_id)
        lower = Items.objects.get(id=o.lower_id)
        foot = Items.objects.get(id=o.foot_id)
        recom.append({
            'id': o.id,
            'upper_path': upper.photo.url,
            'lower_path': lower.photo.url,
            'bottom_path': foot.photo.url,
            'score': o.score,
            'type': o.type,
        })
       
    return recom


def toggle_like_outfit(request, outfit_id):
    outfit = Outfits.objects.get(id=outfit_id)

    outfit.like = not outfit.like
    outfit.save()
    return JsonResponse({'message': 'Like status toggled successfully'})

def toggle_like_items(request, item_id):
    # Fetch the outfit
    item = Items.objects.get(id=item_id)
    user=request.user

    # Toggle the like status
    item.like = not item.like
    item.save()
    return JsonResponse({'message': 'Like status toggled successfully'})

def delete_item(request, item_id):
    # print(item_id)
    item = Items.objects.get(id=item_id,user=request.user)
    item.delete()
    outfits_to_delete = Outfits.objects.filter(
    Q(upper_id=item_id) | Q(lower_id=item_id) | Q(foot_id=item_id),user=request.user)
    
    outfits_to_delete.delete()
    return redirect("/closet/")

def update_item(request, item_id):
    # print(item_id)
    item = Items.objects.get(pk=item_id)
    return render(request, 'update_item.html', {'item':item})

def do_update(request, item_id):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        item_category = request.POST.get("item_category")
        item_color = request.POST.get("item_color")
        if item_category=="Topwear":
            item_pattern=request.POST.get("item_pattern")
        else: item_pattern="null"    
        item_brand = request.POST.get("item_brand")
        item_price = request.POST.get("item_price")
        item_type = request.POST.get("item_type")
        item_photo=request.FILES.get('item_photo')

        item = Items.objects.get(pk=item_id)

        item.name = item_name
        item.user=request.user
        item.category = item_category
        item.color = item_color
        item.pattern=item_pattern
        item.brand = item_brand
        item.price = item_price
        item.type = item_type
        item.photo = item_photo
        item.save()
    return redirect("/closet/")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect("/home/")  # Redirect to your home page after successful signup
        else:
            print(form.errors)
            messages.error(request, 'Invalid form submission. Please check the errors below.')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect("/home/")
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



def scrape_items(request):
    urls = [
        'https://www.google.com/search?tbm=shop&q=red+tshirt+black+shirt',
        'https://www.google.com/search?tbm=shop&q=black+pant+blue+jeans',
        'https://www.google.com/search?tbm=shop&q=blue+nike+shoes'
    ]

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    scrapped_items = {'upper_items': [], 'lower_items': [], 'foot_items': []}

    max_items_per_category = 3

    for url in urls:
        data = requests.get(url, headers=header)
        soup = BeautifulSoup(data.content, 'html.parser')

        category = ''
        if 'shirt' in url:
            category = 'upper_items'
        elif 'pant' in url:
            category = 'lower_items'
        elif 'shoe' in url:
            category = 'foot_items'

        items_added = 0

        for div in soup.find_all('div', class_='sh-dgr__content'):
            if items_added >= max_items_per_category:
                break

            link1 = "https://www.google.com/"
            link_tag = div.find('a', class_='xCpuod')
            link = link1 + link_tag['href'] if link_tag else None

            # Extracting image source
            img_div = div.find('div', class_='ArOc1c')
            img_src = img_div.find('img')
            img_source = img_src.get('src') if img_src else None

            # Extracting header text
            h3_tag = div.find('h3', class_='tAxDx')
            header_text = h3_tag.text.strip() if h3_tag else None

            # Extracting price
            span_tag = div.find('span', class_='a8Pemb OFFNJ')
            price_text = span_tag.text.strip() if span_tag else None

            scrapped_items[category].append({
                'link': link,
                'img_link': img_source,
                'name': header_text,
                'price': price_text
            })

            items_added += 1

    return render(request, 'store.html', {'scrapped_items': scrapped_items})
