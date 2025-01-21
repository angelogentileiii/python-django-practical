from django import forms

from .models import Review

# Can build a new form class and specify all of our input values
# class ReviewForm(forms.Form):
#     user_name = forms.CharField(label="Your Name", max_length=50, error_messages={
#         "required": "This field is required and must not be left empty.",
#         "max_length": "Please enter a name that is 50 characters or less."
#     })
#     review_text = forms.CharField(label="Your Feedback", widget=forms.Textarea, max_length=250)
#     rating = forms.IntegerField(label="Your Rating", min_value=1, max_value=5)

class ReviewForm(forms.ModelForm):
    # Use the nested Meta class to tell Django which model this form should be related to
    class Meta:
        model = Review
        # Tells django that we are going to use all of the fields within the Review class
        #   - Can also use a list to specifiy precisely which fields we want to include
        # If we want to include all fields except a few, we can use the exclude value and a list of the fields to exclude
        fields = '__all__' 

        labels = {
            "user_name": "Your Name",
            "review_text": 'Your Review',
            "rating": "Your Rating"
        }

        error_messages = {
            "required": "This field is required and must not be left empty.",
            "max_length": "Please enter a name that is 50 characters or less."
        }
        