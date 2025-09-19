from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Transaction
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from accounts.decorators import userprofile_login_required


# Create your views here.
@userprofile_login_required
def index(request):
    if request.method == 'POST':
        print("Post Called")
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        if not amount:
            messages.info(request,"Enter Amount")
            return redirect('calculate:index')
        amount = round(float(amount),2)
        print("Amount and description is : ",type(amount),description)
        if description == '':
            messages.info(request,"Enter Description")
            return redirect('calculate:index')
        if type(amount)==str:
            if len(amount)==0:
                messages.info(request,"Amount should not be empty")
                return redirect('calculate:index')
            messages.info(request,"Amount should be in Number")
            return redirect('calculate:index')
        
        trans = Transaction.objects.create(description=description,amount=amount)
        
        return redirect('calculate:index')
    else:
        print("Get Method Called")
    context = {
        "transactions":Transaction.objects.all(),
        'balance':Transaction.objects.all().aggregate(total_balance=Sum('amount'))['total_balance'] or 0,
        'income':Transaction.objects.filter(amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense':Transaction.objects.filter(amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0,
    }
            
    return render(request,'calculate/index.html',context)

def delete_transactions(request,uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('calculate:index')

def delete_all_transactions(request):
    Transaction.objects.all().delete()
    return redirect('calculate:index')