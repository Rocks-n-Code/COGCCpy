import pandas as pd
import requests
import time
import re

class formation_tops:

    def __init__(self, apis):
        self.apis = [x.replace('-', '')[:10] for x in apis]
        state_codes = [x[:2] for x in self.apis if x[:2] != '05']
        if len(state_codes) > 0:
            raise ValueError('State code found outside of Colorado:', state_codes)
        self.df = pd.DataFrame()
        self.pull_tops()
        self.import_fmt_df()

    def top_parse(self, text):
        '''
        Input:
        text; str, html code from COGCC facility detail site.

        Output
        tops; df, DataFrame of formation tops
        '''
        # Create list of DataFrames
        df_list = pd.read_html(text)

        # Select last DF
        tops = df_list[-1]

        # Test for no tops
        if 'Formation' not in tops[0].tolist():
            print('No Tops Found')
            return pd.DataFrame()

        # Set column names
        i = tops[tops[0] == 'Formation'].index.values[0]
        tops.columns = [x.strip().replace(' ', '_') for x in tops.loc[i, :].tolist()]
        tops = tops[i + 1:].reset_index(drop=True)
        tops = tops[1:].reset_index(drop=True)

        # Format Top and Bottom column
        cols = ['Formation', 'Log_Top', 'Log_Bottom', 'Cored', 'DSTs']
        tops = tops[cols]
        for col in cols[1:3]:
            tops[col] = tops[col][tops[col].notnull()].apply(lambda x: re.sub('\D',
                                                                              '',
                                                                              x))
            tops[col] = tops[col].astype(float)

        tops = tops[tops.Formation != 'No formation data to display.']
        return tops

    def pull_tops(self):
        '''
        Pulls tops from COGCC facility pages. Updates self.df
        '''
        baseURL = 'https://cogcc.state.co.us/cogis/FacilityDetail.asp?facid='

        total = len(self.apis)
        i = 0
        for api in self.apis:
            i += 1
            prec = str(int(100 * i / total)) + '% complete  '
            print(api, prec, end='\r')
            try:
                url = baseURL + api.replace('-', '')[2:] #+ tailURL
                r = requests.get(url)

                if r.status_code == 200:
                    formations = self.top_parse(r.text)
                    formations['API'] = api
                    self.df = pd.concat([self.df, formations],
                                      ignore_index=True)
                    time.sleep(5)  # Wait 5 sec.
                else:
                    print(api, ':', r.status_code)
            except Exception as e:
                print('Error:', api, e)

    def import_fmt_df(self):
        df = self.df.copy()
        tops  = sorted(df.Formation[df.Log_Top.notnull()].unique().tolist())
        bases = sorted(df.Formation[df.Log_Top.notnull()].unique().tolist())
        for top in tops:
            df[top.replace(' ','_')] = df.Log_Top[(df.Formation == top)&(df.Log_Top.notnull())]
        for base in bases:
            df[base.replace(' ','_') + '_base'] = df.Log_Bottom[(df.Formation == base)&(df.Log_Bottom.notnull())]

        cols = sorted([x.replace(' ','_') for x in tops] + [x.replace(' ','_') + '_base' for x in bases])
        cols = ['API'] + cols
        self.fmt_df = df