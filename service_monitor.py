import urllib.request
import ast
import json
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import argparse

# author : Kunal J
# date 16 June 2022
# This is monitoring tool that will query Cloud Provider X (CPX) and will fetch the server details with following metrics.
# A. Fetch all running microservices
# B. Print average CPU/Memory of services of the same type 
# c. fetch the services which have fewer than 2 healthy instances running 
# D. print CPU/Memory of all instances of a given service over a time.
 


# function to call CPX API for fetching all running servers
def fetch_all_cpx_servers(port):
    url = "http://localhost:"+port+"/servers"
    # print(url)
    resp = urllib.request.urlopen(url)
    serverNames=resp.read()
    strServerNameList=serverNames.decode('UTF-8')
    ls = strServerNameList.strip('[]').replace('"', '').replace(' ', '').split(',')
    return ls


# This function calls CPX API for fetching individual running server details, it will return JSON string
def fetch_cpx_server_details(ls, str1,port):
    # print(port)
    for i in range(len(ls)):
        resp = urllib.request.urlopen('http://localhost:'+port+'/'+ls[i])
        serverdata=resp.read().decode('UTF-8')
        jsonStr=serverdata.replace("{","{\"IP\":"+"\""+ls[i]+"\",")

        if(len(str1)==0):
            str1=str1+jsonStr
        else:
            str1=str1+","+jsonStr
    return str1

# This uses the json string returned in fetch_cpx_server_details function
# and call CPX API for fetching all running microservices.
def print_running_services(ls, str1):
    df=pd.read_json(str1,lines=True)
    pd.set_option('display.max_rows', len(ls))
    pd.set_option('display.colheader_justify', 'center')
    df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
    df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

    df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
'service':'Service'},inplace = True)
    df['Status'] = 'Healthy'
    df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

    column_names = ['IP','Service', 'Status','CPU','Memory']
    df = df.reindex(columns=column_names)
    df['CPU'] = df['CPU'].astype(str) + '%'
    df['Memory'] = df['Memory'].astype(str) + '%'
    df2 = df.to_string(index=False)
    print (df2)

# This returns the average cpu and memory usage for each microservice
def get_avg_cpumem_usage(ls, str1):
    df=pd.read_json(str1,lines=True)
    pd.set_option('display.max_rows', len(ls))
    pd.set_option('display.colheader_justify', 'center')
    df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
    df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

    df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
'service':'Service'},inplace = True)
    df['Status'] = 'Healthy'
    df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

    column_names = ['IP','Service', 'Status','CPU','Memory']
    df = df.reindex(columns=column_names)
    df.drop('IP', axis=1, inplace=True)
    df_groupedby=df.groupby(['Service','Status'])[['CPU', 'Memory']].mean().round(0)
    df_groupedby['CPU'] = df_groupedby['CPU'].astype(str) + '%'
    df_groupedby['Memory'] = df_groupedby['Memory'].astype(str) + '%'
    print(df_groupedby)


# This reports the microservices which have fewer than 2 healthy instances running 
def topmost_fewer_healthy_instaces(ls, str1):
    df=pd.read_json(str1,lines=True)
    pd.set_option('display.max_rows', len(ls))
    pd.set_option('display.colheader_justify', 'center')
    df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
    df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

    df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
'service':'Service'},inplace = True)
    df['Status'] = 'Healthy'
    df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

    column_names = ['IP','Service', 'Status','CPU','Memory']
    df = df.reindex(columns=column_names)
    df['CPU'] = df['CPU'].astype(str) + '%'
    df['Memory'] = df['Memory'].astype(str) + '%'

    df_filtered=df.query("Status == 'Healthy'")
    df_filtered.drop('CPU', axis=1, inplace=True)
    df_filtered.drop('IP', axis=1, inplace=True)
    df_filtered.drop('Memory', axis=1, inplace=True)
    df_groupedby = df_filtered[df_filtered.groupby(['Service','Status'])['Service'].transform('count') < 2]
    fewer_instances=df_groupedby.groupby(['Service']).agg(['count'])
    print(fewer_instances)


# This reports the microservices which fetches cpu and memory details for provided service type
# it will fetch details continously until it gets interrupted by keyboard 
def print_cpumem_details_service(ls, str1,serviceName=""):
    while True:
        try:
            df=pd.read_json(str1,lines=True)
            pd.set_option('display.max_rows', len(ls))
            pd.set_option('display.colheader_justify', 'center')
            df['cpu'] = pd.to_numeric(df['cpu'].str.replace('%', ''))
            df['memory'] = pd.to_numeric(df['memory'].str.replace('%', ''))

            df.rename(columns = {'IP':'IP', 'cpu':'CPU', 'memory':'Memory',
        'service':'Service'},inplace = True)
            df['Status'] = 'Healthy'
            df.loc[(df['CPU'] >= 80) & (df['Memory'] >= 80), 'Status'] = 'Unhealthy'

            column_names = ['IP','Service', 'Status','CPU','Memory']
            df = df.reindex(columns=column_names)
            df['CPU'] = df['CPU'].astype(str) + '%'
            df['Memory'] = df['Memory'].astype(str) + '%'
            # df.loc[df['Service'] == serviceName]
            df_filtered=df.query("Service ==\""+serviceName+"\"")
            # print(df_filtered)
            df2 = df_filtered.to_string(index=False)
            # df2.query('Service == \"'+serviceName+'\"')
            print (df_filtered)
        except KeyboardInterrupt:
            print("Interrupted")
            break
            

def main(port: str, menuoption: str,serviceName = ""):
    ls = fetch_all_cpx_servers(port)
    str1=''
    str1 = fetch_cpx_server_details(ls, str1,port)

    if menuoption == '1':
        print_running_services(ls, str1)
    elif menuoption == '2':
        get_avg_cpumem_usage(ls, str1)
    elif menuoption == '3':
        topmost_fewer_healthy_instaces(ls, str1)
    elif menuoption =='4':
        print_cpumem_details_service(ls,str1,serviceName)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="the port on which to run", type=str)
    parser.add_argument("menuoption", help="the menu option for extraction", type=str)
    parser.add_argument("serviceName", help="the service name for extraction", type=str)

    args = parser.parse_args()
    main(args.port,args.menuoption,args.serviceName)