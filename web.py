import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

def load_data():
    dataMinyak = pd.read_csv('produksi_minyak_mentah.csv')
    country = pd.read_json('kode_negara_lengkap.json')
    mergeResult = pd.merge(left=country, right=dataMinyak, left_on='alpha-3', right_on='kode_negara')
    data = dataHasil=mergeResult[['name','tahun','produksi','alpha-3','country-code','iso_3166-2','region','sub-region','intermediate-region','region-code','sub-region-code']]
    data2 = data.rename({'name': 'Negara','produksi':'Produksi' ,'tahun': 'Tahun','alpha-3':'Kode Negara','region':'Region','sub-region':'Sub Region'}, axis='columns')
    return data2
def get_total_dataframe(dataset):
    total_dataframe = dataset[['Negara','Tahun','Kode Negara','Region','Sub Region','Produksi']]
    return total_dataframe

dataset=load_data()
dataset_bersih = dataset[dataset['Produksi'] != 0]
dataset_tidak_produksi = dataset[dataset['Produksi'] == 0]
st.header("ANALISA DATA PRODUKSI MINYAK DI SELURUH NEGARA")

data_select_negara = dataset_bersih.groupby('Negara',as_index=False).mean()
select = st.selectbox('Pilih negara',data_select_negara['Negara'])
negara_data = dataset[dataset['Negara'] == select]
if select:
    state_total = get_total_dataframe(negara_data)

    st.subheader("Grafik pendapatan minyak negara "+select)
    state_total_graph = px.bar(state_total, x='Tahun',y='Produksi',labels="Grafik pendapatan minyak",color='Produksi')
    st.plotly_chart(state_total_graph,use_container_width=True)

st.subheader("NEGARA DENGAN NILAI KUMULATIF PRODUKSI TERTINGGI")
nilai_cum = st.slider("Geser slider ke kanan", min_value=1, max_value=10, value=1)
Data = dataset[['Negara','Kode Negara','Tahun','Produksi','Region','Sub Region']]
Data['Produksi Kumulatif'] = Data['Produksi'].cumsum()
total = Data.sort_values(by=['Produksi Kumulatif'],ascending=False)
urut = total.groupby('Negara',as_index=False).sum()
dataMax = urut.sort_values(by=['Produksi'],ascending=False).head(nilai_cum)
bar_chart = px.bar(dataMax, x='Negara',y='Produksi',color='Negara')
st.plotly_chart(bar_chart,use_container_width=True)


st.subheader("GRAFIK PENDAPATAN MINYAK BERDASARKAN TAHUN")
select_year = st.selectbox("Lihat Tahun",dataset['Tahun'])
if select_year:
    
    state_year = dataset[dataset['Tahun'] == select_year]
    state_total = get_total_dataframe(state_year)
    st.markdown("Tampilan Negara tertinggi Penghasil Minyak pada tahun "+str(select_year))
    nilai = st.slider("Geser slider untuk menampilkan jumlah data", min_value=1, max_value=10, value=1)
    dataMax = state_total.sort_values(by=['Produksi'],ascending=False).head(nilai)
    dataf = dataMax[['Negara','Tahun','Produksi']]
    max_data = px.bar(dataf, x='Negara',y='Produksi',color='Negara',labels={'Jumlah':'Produksi tahun %s' % (select_year)})
    st.plotly_chart(max_data,use_container_width=True)

    st.markdown("Negara Produksi tertinggi pada tahun "+str(select_year))
    data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
    data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].max()]
    st.dataframe(data_tahun[["Negara",'Kode Negara',"Tahun","Produksi",'Region','Sub Region']])

    st.markdown("Negara Produksi terendah pada tahun "+str(select_year))
    data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
    data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].min()]
    st.dataframe(data_tahun[["Negara",'Kode Negara',"Tahun","Produksi",'Region','Sub Region']])

    st.markdown("Negara tidak berproduksi pada tahun "+str(select_year))
    data_tahun =dataset_tidak_produksi[dataset_tidak_produksi["Tahun"] == select_year]
    st.dataframe(data_tahun[["Negara",'Kode Negara',"Tahun","Produksi",'Region','Sub Region']])

st.markdown("Negara tidak produksi di sepanjang tahun")
st.dataframe(dataset_tidak_produksi)
    

st.markdown(" <style>footer {visibility: hidden;}</style> ", unsafe_allow_html=True)
