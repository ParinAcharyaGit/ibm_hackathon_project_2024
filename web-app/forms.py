from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired

class PredictForm(FlaskForm):
    burnRate = DecimalField('Burn Rate', validators=[DataRequired()])
    revenue = DecimalField('Revenue', validators=[DataRequired()])
    customerAcquisitionCost = DecimalField('Customer Acquisition Cost', validators=[DataRequired()])
    customerLifetimeValue = DecimalField('Customer Lifetime Value', validators=[DataRequired()])
    monthlyRecurringRevenue = DecimalField('Monthly Recurring Revenue', validators=[DataRequired()])
    churnRate = DecimalField('Churn Rate (%)', validators=[DataRequired()])
    marketGrowthRate = DecimalField('Market Growth Rate (%)', validators=[DataRequired()])
    marketingSpend = DecimalField('Marketing Spend', validators=[DataRequired()])
    rdSpend = DecimalField('R&D Spend', validators=[DataRequired()])
    profitMargin = DecimalField('Profit Margin (%)', validators=[DataRequired()])
    averageEmployeeSalary = DecimalField('Average Employee Salary', validators=[DataRequired()])
    
    submit = SubmitField('Predict')
    
    abc = ""  # This is a regular variable, not a form field, used for the prediction output
