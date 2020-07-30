import pandas as pd
import requests
import time

class production:
    '''
    Access production from COGCC.
    '''

    def __init__(self, apis):
        self.apis = [x.replace('-', '') for x in apis]

        # Check for only APIs only in Colorado
        state_codes = [x[:2] for x in self.apis if x[:2] != '05']
        if len(state_codes) > 0:
            raise ValueError('State code found outside of Colorado:', state_codes)

        self.df = pd.DataFrame()
        self.pull_iterator()

    def pull_iterator(self):
        '''
        Iterates through APIs, seperates components, and sends them to be pulled.
        '''
        total = len(self.apis)
        i = 0

        for api in self.apis:
            i += 1
            prec = str(int(100 * i / total)) + '% complete  '
            print(api, prec, end='\r')

            # Testing so far shows that the "APIWB" and "Year" do not limit results.
            api_wb = 'All'
            year = 'All'

            # County code
            api_co = api[2:5]

            # Well code
            api_well = api[5:10]

            self.pull_prod(api_co, api_well, api_wb, year)
            time.sleep(5)

    def pull_prod(self, api_co, api_well, api_wb, year):
        '''
        Pulls production data from COGCC.
        '''
        url = 'https://cogcc.state.co.us/production/?&apiCounty=' + api_co + '&apiSequence=' + api_well + '&APIWB=' + api_wb + '&Year=' + year
        r = requests.get(url)
        if r.status_code == 200:
            if 'No Records found' not in r.text:
                df = pd.read_html(r.text)[1]

                ##Format Columns
                cols = ['Days Produced', 'BOM Inventory', 'Oil Produced', 'Oil Sold', 'Oil Adjustment', 'EOM Inventory',
                        'Oil Gravity', 'Gas Produced', 'Gas Flared', 'Gas Sold', 'Gas Used', 'Water Volume']
                for col in cols:
                    df[col].fillna(0, inplace=True)
                    df[col] = df[col].astype(int)

                df['First of Month'] = pd.to_datetime(df['First of Month'])

                # Format API Codes
                df['API County'] = df['API County'].astype(str)
                df['API County'] = df['API County'].apply(lambda x: '{0:0>3}'.format(x))

                df['API Sequence'] = df['API Sequence'].astype(str)
                df['API Sequence'] = df['API Sequence'].apply(lambda x: '{0:0>5}'.format(x))

                df['API Sidetrack'] = df['API Sidetrack'].astype(str)
                df['API Sidetrack'] = df['API Sidetrack'].apply(lambda x: '{0:0>2}'.format(x))

                # Set API_Label Column
                df['API_Label'] = '05-' + df['API County'] + '-' + df['API Sequence'] + '-' + df['API Sidetrack']

                # Reorder with Flexibility
                cols = list(df)
                cols.remove('API_Label')
                cols = ['API_Label'] + cols
                df = df[cols]

                self.df = pd.concat([self.df, df], ignore_index=True)

        else:
            print('Bad Response:', r.status_code)