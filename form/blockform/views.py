from django.views.generic import TemplateView
from django.shortcuts import render
import datetime
from django.db.models import Sum

import requests


from blockform.forms import HomeForm
from blockform.models import Address, Transaction

class HomeView(TemplateView):
    template_name = 'home/home.html'

    # GET request handler
    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    #POST request handler
    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['post']
            dateFrom = form.cleaned_data['dateFrom']
            dateTo = form.cleaned_data['dateTo']
            #checking if address is in database
            isInDatabase = Address.objects.filter(address=value)
            if isInDatabase:
                #query database for given address
                addressData = Address.objects.filter(address=value)
                id = Address.objects.values_list('id', flat=True).get(address=value)
                #checking if date range is applied
                if (dateFrom != None and dateTo != None):
                     trData = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo ))
                     counter = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo )).count()
                     positiveSum = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo )).aggregate(Sum('output'))
                     negativeSum = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo )).aggregate(Sum('negativeoutput'))
                     sum = positiveSum['output__sum'] - negativeSum['negativeoutput__sum']


                else:
                    trData = Transaction.objects.filter(addressRel = id)
                    counter = Transaction.objects.filter(addressRel = id).count()
                    sum = None



            else:
                #get data from API
                url = 'https://blockchain.info/rawaddr/%s' % value
                response = requests.get(url)
                data = response.json()

                #collect address data and save to the database
                address = data['address']
                n_tx = data['n_tx']
                total_received = data['total_received']
                total_sent = data['total_sent']
                final_balance = data['final_balance']

                addr = Address(address = address, n_tx = n_tx, total_received = total_received,
                total_sent = total_sent, final_balance = final_balance)

                addr.save()

                #collect transactions data and save to the database
                for tx in data['txs']:

                    def output(tx, address):
                        for o in tx['out']:
                            if o['addr'] == address:
                                return o['value']
                    def negativeoutput(tx, address):
                        for i in tx['inputs']:
                            if i['prev_out']['addr'] == address:
                                return i['prev_out']['value']

                    tx_id = tx['hash']
                    size = tx['size']
                    weight = tx['weight']
                    time = datetime.datetime.fromtimestamp(tx['time'])
                    addressRel = address
                    relOutput = output(tx, address)
                    relNegOutput = negativeoutput(tx, address)


                    trans = Transaction(tx_id = tx_id, size = size, weight = weight, time = time, addressRel = addr, output=relOutput, negativeoutput=relNegOutput)
                    trans.save()

                    #query database for given address
                    addressData = Address.objects.filter(address=value)
                    id = Address.objects.values_list('id', flat=True).get(address=value)
                    #checking if date range is applied
                    if (dateFrom != None and dateTo != None):
                         trData = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo ))
                         counter = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo )).count()
                         positiveSum = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo )).aggregate(Sum('output'))
                         negativeSum = Transaction.objects.filter(addressRel = id).filter(time__range=(dateFrom, dateTo )).aggregate(Sum('negativeoutput'))
                         sum = positiveSum['output__sum'] - negativeSum['negativeoutput__sum']

                    else:
                        trData = Transaction.objects.filter(addressRel = id)
                        counter = Transaction.objects.filter(addressRel = id).count()

                        sum = None




        #return data to the user
        args = {'form': form, 'addressData': addressData, 'trData': trData, 'counter': counter, 'sum': sum,}
        return render(request, self.template_name, args)
