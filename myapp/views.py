from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from operator import itemgetter
from .models import Items, Outfits
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


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
    items = Items.objects.all()

    return render(request, "closet.html", {'items':items})

def add_item(request):
    if request.method=='POST':

        #fetch kar rahe data ko idhar
        item_name = request.POST.get("item_name")
        item_category = request.POST.get("item_category")
        item_color = request.POST.get("item_color")
        item_brand = request.POST.get("item_brand")
        item_price = float(request.POST.get("item_price"))
        item_type = request.POST.get("item_type")
        # item_photo = request.POST.get("item_photo")
        item_photo=request.FILES.get('item_photo')

        # print(item_photo)

        #model ka object bana rahe idhar
        item = Items()
        item.name = item_name
        item.category = item_category
        item.color = item_color
        item.brand = item_brand
        item.price = item_price
        item.type = item_type
        item.photo = item_photo


        item.save()

        return redirect("/closet/")
    return render(request, 'add_item.html', {})

def calculate_score(upper, lower, bottom):
    TShirt= {
        'red': 18,
        'dark red': 18,
        'white': 18,
        'black': 20,
        'blue': 18,
        'dark-blue': 20,
        'yellow': 10,
        'green': 14,
        'sky-blue': 15,
        'light green': 12,
        'pink': 16,
        'purple': 17,
        'orange': 15,
        'brown': 15,
        'grey': 18
    }
    
    Shirt= {
        'red': 17,
        'white': 20,
        'black': 20,
        'blue': 18,
        'dark-blue': 19,
        'yellow': 10,
        'green': 14,
        'sky-blue': 18,
        'light green': 16,
        'pink': 17,
        'purple': 15,
        'orange': 15,
        'brown': 17,
        'grey': 18
    }

    Pant= {
        'red': 8,
        'white': 17,
        'black': 20,
        'blue': 20,
        'dark-blue': 20,
        'yellow': 6,
        'green': 15,
        'sky-blue': 17,
        'light green': 6,
        'pink': 10,
        'purple': 11,
        'orange': 8,
        'brown': 17,
        'grey': 19,
        'cream': 18
    }

    Shoes= {
        'red': 9,
        'dark-blue': 15,
        'white': 15,
        'black': 15,
        'yellow': 9,
        'green': 1,
        'sky-blue': 15,
        'light green': 9,
        'pink': 15,
        'purple': 15,
        'orange': 15,
        'brown': 10,
        'grey': 15
    }

    Dress= {
        'red': 19,
        'dark-blue': 18,
        'white': 20,
        'black': 20,
        'yellow': 17,
        'green': 17,
        'sky-blue': 19,
        'light green': 17,
        'pink': 18,
        'purple': 19,
        'orange': 17,
        'brown': 16,
        'grey': 19
    }

#pants on dress like kurta
    Dpants= {
        'red': 8,
        'dark-blue': 15,
        'white': 18,
        'black': 18,
        'yellow': 7,
        'green': 7,
        'sky-blue': 15,
        'light green': 6,
        'pink': 7,
        'purple': 14,
        'orange': 9,
        'brown': 9,
        'grey': 15,
        'blue': 18,
        'cream': 18
    }
        
    Jacket= {
        'red': 12,
        'dark blue': 20,
        'white': 20,
        'black': 20,
        'yellow': 12,
        'green': 14,
        'sky blue': 18,
        'light green': 11,
        'pink': 15,
        'purple': 17,
        'orange': 11,
        'brown': 15,
        'grey': 18,
        'cream': 15
    }

    color_theme = {
        "red": "b",
        "dark blue": "d",
        "blue": "b",
        "green": "b",
        "yellow": "b",
        "black": "d",
        "white": "l",
        "purple": "d",
        "orange": "b",
        "pink": "b",
        "grey": "l",
        "sky blue": "l",
        "brown": "d",
        "cream": "l"
    }

    
    upper_color = upper.color
    lower_color = lower.color
    bottom_color = bottom.color
    upper_type = upper.name
    lower_type = lower.name
    bottom_type= bottom.name


    lower_color_scores= Pant
    bottom_color_scores=Shoes

    if(upper_type=='T-Shirt'):
        upper_color_scores= TShirt
    elif(upper_type=='Dress'):
        upper_color_scores= Dress
        lower_color_scores= Dpants
    else:
        upper_color_scores= Shirt
    
    upper_theme= color_theme.get(upper_color)
    lower_theme=color_theme.get(lower_color)
    bottom_theme=color_theme.get(bottom_color)

    # Calculate color score based on color popularity
    #ha formula change karaycha ahe ajun multiplying factor use karaycha ahe like upper theme dark asel tr lower theme pn dark pahije so greater value milel, else value normal rahil, similar for upper light and lower dark, bottom dark hya combination la jast value dyaychi/kiti asli pahije...etc etc    
    # color_score = upper_color_scores.get(upper_color, 3) + lower_color_scores.get(lower_color, 3) + bottom_color_scores.get(bottom_color, 3)

    if(upper.type ==lower.type ==bottom.type ):
        color_score = upper_color_scores.get(upper_color) + lower_color_scores.get(lower_color) + bottom_color_scores.get(bottom_color)
    elif(upper.type ==lower.type =="Formal" and (bottom.type =="Casual" or bottom.type =="Ocassional")):
        color_score = upper_color_scores.get(upper_color) + lower_color_scores.get(lower_color) + (bottom_color_scores.get(bottom_color) * 0.5)
    elif(upper.type =="Formal" and lower.type =="Casual" and (bottom.type =="Casual" or bottom.type =="Formal")):
        color_score = upper_color_scores.get(upper_color) + (lower_color_scores.get(lower_color) * 0.6)+ (bottom_color_scores.get(bottom_color))
    elif(upper.type =="Ocassional" and lower.type =="Formal" and (bottom.type =="Ocassional" or bottom.type =="Formal")):
        color_score = upper_color_scores.get(upper_color) + (lower_color_scores.get(lower_color) * 0.5)+ (bottom_color_scores.get(bottom_color))
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
    items = Items.objects.all()
    outfits = []
    for upper in items:
        if upper.category == 'Topwear':
            for lower in items:
                if lower.category == 'Bottomwear':
                    for bottom in items:
                        if bottom.category == 'Footwear':
                            outfit = Outfits()
                            # outfit.upper_name = upper.name
                            outfit.upper_path = upper.photo
                            # outfit.upper_color = upper.color
                            # outfit.lower_name= lower.name
                            outfit.lower_path= lower.photo
                            # outfit.lower_color= lower.color
                            # outfit.bottom_name= bottom.name
                            outfit.bottom_path= bottom.photo
                            # outfit.bottom_color = bottom.color
                            outfit.type = calc_type(upper.type, lower.type, bottom.type)
                            outfit.score = calculate_score(upper, lower, bottom)
                            outfit.save()
                            if outfit.score>0:
                                outfits.append({
                                'id': outfit.id,
                                'upper_path': outfit.upper_path.url,
                                'lower_path': outfit.lower_path.url,
                                'bottom_path': outfit.bottom_path.url,
                                'type': outfit.type,
                                'score': outfit.score,
                                })
                                print("Added outfit:", outfit)
    sorted_outfits = sorted(outfits, key=lambda outfit: outfit['score'], reverse=True)
                                                    
    return sorted_outfits


from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# def content_based_recommendation_for_user(user_profile, n_recommendations=10):
#     # Get all items from the database
#     all_items = Items.objects.all()

#     # Extract attributes from items
#     item_names = [item.name for item in all_items]
#     item_features = [[item.category, item.color, item.brand, item.type] for item in all_items]

#     # Convert text attributes (name) into numerical features using TF-IDF
#     name_vectorizer = TfidfVectorizer()
#     name_features = name_vectorizer.fit_transform(item_names).toarray()  # Convert to dense array

#     # Preprocess categorical features
#     categorical_features = [0, 1, 2, 3]  # Indices of categorical features
#     categorical_transformer = OneHotEncoder()  # One-hot encoding for categorical features

#     # Define column transformer to apply different transformations to different columns
#     preprocessor = ColumnTransformer(
#         transformers=[
#             ('cat', categorical_transformer, categorical_features)
#         ],
#         remainder='passthrough'  # Pass numerical features unchanged
#     )

#     # Define pipeline to apply preprocessing steps
#     pipeline = Pipeline([
#         ('preprocessor', preprocessor)
#     ])

#     # Apply preprocessing to item features
#     item_features_processed = pipeline.fit_transform(item_features).toarray()  # Convert to dense array

#     # Combine text and numerical features
#     combined_features = np.hstack((name_features, item_features_processed))

#     # Ensure user profile has the same number of features and reshape to 2D array
#     user_profile = np.array(user_profile).reshape(1, -1)  # Reshape to ensure 2D array with same number of features

#     # Print shapes for debugging
#     print("Shape of user_profile:", user_profile.shape)
#     print("Shape of combined_features:", combined_features.shape)


#     # Get feature names for text features (TF-IDF)
#     text_feature_names = name_vectorizer.get_feature_names_out()

#     # Get feature names for categorical features (One-Hot Encoding)
#     categorical_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out()

#     # Combine feature names
#     combined_feature_names = np.concatenate((text_feature_names, categorical_feature_names))

#     # Print feature names for text features (TF-IDF)
#     print("Text Feature Names:")
#     print(text_feature_names)

#     # Print feature names for categorical features (One-Hot Encoding)
#     print("\nCategorical Feature Names:")
#     print(categorical_feature_names)

#     # Print combined feature names
#     print("\nCombined Feature Names:")
#     print(combined_feature_names)


#     # Calculate cosine similarity between user profile and items
#     user_item_similarity = cosine_similarity(user_profile, combined_features)

#     # Get indices of top-N most similar items
#     if user_item_similarity.ndim > 1:  # Check if similarity is calculated
#         top_n_indices = np.argsort(user_item_similarity[0])[::-1][:n_recommendations]
#         # Recommend items
#         recommended_items = [all_items[i] for i in top_n_indices]
#     else:
#         recommended_items = []

#     return recommended_items


# def recommend_items(request):
#     # Retrieve user profile from request, session, or database
    
#     user_profile = [0,0,0,0]

#     # Generate recommendations based on user profile
#     recommended_items = content_based_recommendation_for_user(user_profile)

#     # Pass recommended items to template
#     context = {
#         'recommended_items': recommended_items
#     }

#     # Render response
#     return render(request, 'recommendations.html', context)

def outfits(request):
    outfits = make_outfits(request)
    # top_outfits = sorted(outfits, key=itemgetter('Score'), reverse=True)[:3]
    # print(top_outfits)
    return render(request, 'outfits.html', {'outfits': outfits})

def delete_item(request, item_id):
    # print(item_id)
    item = Items.objects.get(pk=item_id)
    item.delete()
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
        item_brand = request.POST.get("item_brand")
        item_price = request.POST.get("item_price")
        item_type = request.POST.get("item_type")
        item_photo=request.FILES.get('item_photo')

        item = Items.objects.get(pk=item_id)

        item.name = item_name
        item.category = item_category
        item.color = item_color
        item.brand = item_brand
        item.price = item_price
        item.type = item_type
        item.photo = item_photo

        item.save()
    return redirect("/closet/")



def signup(request):
    pass

def login(request):
    pass
