# used to get commission data from Commission Junction 
# Requires the following parameters -

# Start date
# End date [The total interval cannot be more than 31 days]
# aids list - This is the list of the advertiser id whose data you want

# The script will return a dict with the total commission for each AID

from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from BeautifulSoup import BeautifulSoup
import logging

log = logging.getLogger()

class CJ(object):

    URL_ENDPOINT = 'https://commission-detail.api.cj.com/v3/commissions'

    def __init__(self, key, end_date = None, start_date = None, aids = []):
	assert key, 'developer key is required'
	self.key = key
	self.end_date = end_date if end_date else datetime.utcnow()
	self.start_date = start_date if start_date else (self.end_date + relativedelta(days = -31))
	self.aids = aids
    
    def _make_url(self, start_date, end_date):
	url = '%s?date-type=event&start-date=%s&end-date=%s' %(self.URL_ENDPOINT,
		start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
	if self.aids:
	    url = '%s?aids=%s' %(url, ','.join(self.aids))
	return url
    
    def _extract_error(self, response):
	return BeautifulSoup(response).find('error-message').renderContents()

    def _get_commission_list(self, response):
	response = BeautifulSoup(response)
	if int(response.find('commissions').get('total-matched')) > 0:
	    return response.findAll('commission')
	else:
	    return []

    def _get_aid_amount_map(self, c):
	return {
		'aid' : c.find('aid').renderContents(),
		'commission_amount' : float(c.find('commission-amount').renderContents())
	       }

    def _make_dates(self):
	res = []
	if (self.end_date - self.start_date).days > 31:
	    res = self._split_dates(start_date = self.start_date, 
		    end_date = self.end_date)
	else:
	    res = [{'start_date' : self.start_date, 'end_date' : self.end_date}]
	return res

    def _split_dates(self, start_date, end_date):
	res = []
	while (end_date - start_date).days > 31:
	    tmp = {
		    'end_date' : end_date,
		    'start_date' : end_date + relativedelta(days = -31)
		  }
	    res.append(tmp)
	    end_date = tmp.get('start_date') + relativedelta(days = -1)
	res.append({'end_date' : end_date, 'start_date' : start_date})
	return res
    
    '''Call this method to retrieve the commission report
    '''
    def retrieve(self):
	res = {}
	dates_l = self._make_dates()
	for dates in dates_l:
	    r = requests.get(url = self._make_url(start_date = dates.get('start_date'), 
		end_date = dates.get('end_date')), headers = {'authorization' : self.key})
	    if r.ok:
		commission_list = self._get_commission_list(response = r.content)
		for commission in commission_list:
		    m = self._get_aid_amount_map(c = commission)
		    if m.get('aid') in res:
			res[m.get('aid')] = res[m.get('aid')] + m.get('commission_amount')
		    else:
			res[m.get('aid')] = m.get('commission_amount')
	    else:
		raise Exception(self._extract_error(response = r.content))
	return res


if __name__ == '__main__':
    key = 'YOUR-CJ-KEY' # Replace your key here

    # First Test
    end_date = datetime.utcnow()
    start_date = datetime.utcnow() + relativedelta(days = -1)
    log.info('start_date: %s, end_date: %s' %(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    cj = CJ(key = key, end_date = end_date, start_date = start_date, aids = ['10885795', '10694956'])
    log.info(cj.retrieve())

    # Second Test
    log.info('\n\nNo dates specified')
    cj = CJ(key = key)
    log.info(cj.retrieve())

    # Third Test
    end_date = datetime.utcnow()
    start_date = datetime.utcnow() + relativedelta(days = -45)
    log.info('\n\nstart_date: %s, end_date: %s' %(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    cj = CJ(key = key, end_date = end_date, start_date = start_date)
    log.info(cj.retrieve())

    # Fourth Test
    end_date = datetime.utcnow() + relativedelta(days = -10)
    start_date = end_date + relativedelta(days = -103)
    log.info('\n\nstart_date: %s, end_date: %s' %(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    cj = CJ(key = key, end_date = end_date, start_date = start_date)
    log.info(cj.retrieve())

