# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    upper_fav_colors = forms.MultipleChoiceField(
        choices=[('black', 'Black'), ('white', 'White'), ('grey', 'Grey'), ('brown', 'Brown'),('blue', 'Blue'),('navy blue', 'Navy Blue'),('green', 'Green'),('purple', 'Purple'),('cream', 'Cream'),('multi', 'Multi'),('teal', 'Teal'),('charcoal', 'Charcoal'),('lavender', 'Lavender'),('multi', 'Multi'),('lime green', 'Lime Green')],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,  # Allow no selection
    )
    lower_fav_colors = forms.MultipleChoiceField(
        choices=[('black', 'Black'), ('white', 'White'), ('grey', 'Grey'), ('brown', 'Brown'),('blue', 'Blue'),('navy blue', 'Navy Blue'),('green', 'Green'),('purple', 'Purple'),('cream', 'Cream'),('multi', 'Multi'),('teal', 'Teal'),('charcoal', 'Charcoal'),('lavender', 'Lavender'),('multi', 'Multi'),('lime green', 'Lime Green')],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,  # Allow no selection
    )
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'upper_fav_colors', 'lower_fav_colors')

    def save(self, commit=True):
        colorList=["blue","cyan","white","navy blue","green","black","grey","red","pink","brown","beige","yellow","maroon","olive","orange","purple","peach","cream","teal","mustard","multi","burgandy","charcoal","lavender","coral","magenta","lime green","silver","gold","metalic"]
        colorValue1=[8,7,8.5,8,7,8.5,7,8,6,6,7.5,7.5,8,8,8,8,7.5,7.5,7,7,8,7.8,8,8,6,7.5,8,7,7,7]
        colorValue2=[8.5,7,8,8.5,6,8.5,8,6,6,6.5,7,6,7,7,6,7.5,6,7.5,7,7,8,7.5,8,7.7,6,7.6,7.6,7,7,7]
        user = super().save(commit=False)
        if commit:
            user.save()

            # Create or update user profile with color fields
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            upper_fav_colors = self.cleaned_data['upper_fav_colors']
            lower_fav_colors = self.cleaned_data['lower_fav_colors']

            for color in upper_fav_colors:
                index = colorList.index(color)
                colorValue1[index]+=0.5
            user_profile.upper_fav_colors = colorValue1
            for color in lower_fav_colors:
                index=colorList.index(color)
                colorValue2[index]+=0.5
            user_profile.lower_fav_colors = colorValue2                
            user_profile.save()

        return user
    