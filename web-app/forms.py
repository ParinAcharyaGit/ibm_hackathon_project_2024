from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

class PredictForm(FlaskForm):
    age = DecimalField('Age', validators=[DataRequired()])
    contract_length = SelectField('Contract Length', choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')], validators=[DataRequired()])
    customer_id = DecimalField('Customer ID', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    last_interaction = DecimalField('Last Interaction', validators=[DataRequired()])
    payment_delay = DecimalField('Payment Delay', validators=[DataRequired()])
    subscription_type = SelectField('Subscription Type', choices=[('basic', 'Basic'), ('premium', 'Premium'), ('family', 'Family')], validators=[DataRequired()])
    support_calls = IntegerField('Support Calls', validators=[DataRequired()])
    tenure = DecimalField('Tenure (Months)', validators=[DataRequired()])
    total_spend = DecimalField('Total Spend', validators=[DataRequired()])
    usage_frequency = DecimalField('Usage Frequency', validators=[DataRequired()])

    submit = SubmitField('Predict')

    abc = ""  # This is a regular variable, not a form field, used for the prediction output

class ChatForm(FlaskForm):
    message = TextAreaField('Enter a message:', validators=[DataRequired()])
    document = FileField('Upload a document (optional):')
    submit = SubmitField('Submit')