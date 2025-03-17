from django import template
from django.utils import timezone
from ..models import Staff_leave
from datetime import datetime

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary using the key"""
    return dictionary.get(str(key))

@register.filter(name='term_total')
def term_total(fee_data, term_number):
    """Calculates total fees for a specific term"""
    try:
        # Convert both to strings for comparison
        return sum(fee['amount'] for fee in fee_data if str(fee['term']) == str(term_number))
    except (TypeError, KeyError):
        return 0

@register.filter
def has_approved_leave(staff_id, selected_date):
    """Check if staff has approved leave on the given date"""
    try:
        if not selected_date:
            return False
            
        # Convert string date to datetime if needed
        if isinstance(selected_date, str):
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            
        # Debug logging
        print(f"Checking leave for staff {staff_id} on {selected_date}")
        
        has_leave = Staff_leave.objects.filter(
            staff_id=staff_id,
            start_date__lte=selected_date,
            end_date__gte=selected_date,
            status='Approved',
            academic_year__current_ay=True  # Only check current academic year
        ).exists()
        
        print(f"Staff {staff_id} has leave on {selected_date}: {has_leave}")
        return has_leave
        
    except Exception as e:
        print(f"Error checking leave for staff {staff_id}: {str(e)}")
        return False 