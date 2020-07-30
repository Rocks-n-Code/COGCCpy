import pandas as pd
import requests
import time

class formation_tops:

    def __init__(self, apis):
        self.apis = [x.replace('-', '')[:10] for x in apis]
        state_codes = [x[:2] for x in self.apis if x[:2] != '05']
        if len(state_codes) > 0:
            raise ValueError('State code found outside of Colorado:', state_codes)
        self.df = pd.DataFrame()
        self.pull_tops()

    def top_parse(self, text):
        tops = text.split('<!-- LOOP FOR EACH Formation WITHIN WELLBORE -->')[1].split('<!-- END Formation LOOP -->')[0]
        tops = tops.replace('\r', '').replace('\n', '').replace('\t', '').strip()
        tops = tops.split('<tr>')
        tops = [x.strip() for x in tops if len(x) > 0]

        formations = {}
        for top in tops:
            cols = top.split('<td')
            cols = [x.strip() for x in cols if len(x) > 0]
            formation = cols[0].split('color="Navy">')[1].split(' ')[0]
            depth = eval(cols[1].split('<font size="2">')[1].split('</font>')[0])
            formations[formation] = depth
        return formations

    def pull_tops(self):
        baseURL = 'https://cogcc.state.co.us/cogis/FacilityDetail.asp?facid='
        tailURL = '&type=WELL'

        total = len(self.apis)
        i = 0
        for api in self.apis:
            i += 1
            prec = str(int(100 * i / total)) + '% complete  '
            print(api, prec, end='\r')
            try:
                url = baseURL + api.replace('-', '')[2:] + tailURL
                r = requests.get(url)

                if r.status_code == 200:
                    formations = self.top_parse(r.text)
                    formations['API'] = api
                    self.df = self.df.append(formations, ignore_index=True)
                    time.sleep(5)  # Wait 5 sec.
                else:
                    print(api, ':', r.status_code)
            except Exception as e:
                print('Error:', api, e)