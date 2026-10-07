"""Portable Netflix extract → transform → load project pipeline."""
import argparse,json,sqlite3
from pathlib import Path
import pandas as pd

def transform(frame):
    frame=frame.copy();frame.columns=frame.columns.str.strip().str.lower().str.replace(' ','_')
    required={'show_id','type','title','director','cast','country','date_added','release_year','rating','duration','listed_in'}
    if not required<=set(frame.columns):raise ValueError('Missing columns: '+', '.join(sorted(required-set(frame.columns))))
    frame=frame.dropna(subset=['show_id','title']).drop_duplicates('show_id').copy()
    for name,default in [('director','Unknown'),('cast','Not Listed'),('country','Unknown'),('rating','Unknown'),('duration','Unknown')]:
        frame[name]=frame[name].fillna(default).astype(str).str.strip()
        frame.loc[frame[name]=='',name]=default
    frame['date_added']=pd.to_datetime(frame.date_added.astype(str).str.strip(),format='%B %d, %Y',errors='coerce')
    frame=frame.dropna(subset=['date_added']).copy()
    frame['release_year']=pd.to_numeric(frame.release_year,errors='coerce')
    frame=frame.dropna(subset=['release_year'])
    frame['release_year']=frame.release_year.astype(int)
    frame['type']=frame.type.astype(str).str.strip().str.title()
    if not set(frame.type)<={'Movie','Tv Show'}:raise ValueError('Unexpected content type')
    frame['type']=frame.type.replace({'Tv Show':'TV Show'})
    frame['added_year']=frame.date_added.dt.year;frame['added_month']=frame.date_added.dt.month
    frame['years_since_release']=frame.added_year-frame.release_year
    frame['is_movie']=(frame.type=='Movie').astype(int)
    return frame.reset_index(drop=True)

def load(frame,connection):
    with connection:
        frame.to_sql('fact_netflix',connection,if_exists='replace',index=False)
        connection.execute('CREATE UNIQUE INDEX IF NOT EXISTS netflix_show_id ON fact_netflix(show_id)')
    return connection.execute('SELECT COUNT(*) FROM fact_netflix').fetchone()[0]

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',type=Path,default=Path(__file__).parent/'netflix_titles.csv')
    p.add_argument('--database',default=':memory:');p.add_argument('--report',type=Path,default=Path('etl_report.json'))
    a=p.parse_args();raw=pd.read_csv(a.data);clean=transform(raw)
    with sqlite3.connect(a.database) as db:
        count=load(clean,db)
        # Running the same load twice must not append duplicate records.
        again=load(clean,db);assert count==again==len(clean)
        types=dict(db.execute('SELECT type,COUNT(*) FROM fact_netflix GROUP BY type').fetchall())
    a.report.write_text(json.dumps({'input_rows':len(raw),'clean_rows':count,'discarded_rows':len(raw)-count,'counts_by_type':types,'rerun_idempotent':True},indent=2),encoding='utf-8')
    print(count,types)
if __name__=='__main__':main()
