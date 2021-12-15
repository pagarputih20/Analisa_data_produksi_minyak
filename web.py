import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")
st.header("Pusat Informasi Negara Penghasil Minyak")

data_produksi_minyak = pd.read_csv('produksi_minyak_mentah.csv')
data_kode_negara = pd.read_json('kode_negara_lengkap.json')
mergeResult = pd.merge(left=data_kode_negara, right=data_produksi_minyak, left_on='alpha-3', right_on='kode_negara')
dataframe = dataHasil=mergeResult[['name','tahun','produksi','alpha-3','country-code','iso_3166-2','region','sub-region','intermediate-region','region-code','sub-region-code']]
dataset = dataframe.rename({'name': 'Negara','produksi':'Produksi' ,'tahun': 'Tahun','alpha-3':'Kode'}, axis='columns')


lihat_data = st.button('Lihat data awal')
if lihat_data:
     st.subheader("Produksi minyak paling tinggi:")
     info_data = dataset[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     hasil = info_data[info_data['Produksi']==info_data['Produksi'].max()]
     st.dataframe(hasil)
        
     
     Data=dataset[dataset['Negara']=='Saudi Arabia']
     Data = Data[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     Data['Produksi Kumulatif'] = Data['Produksi'].cumsum()
     total = Data[Data['Produksi Kumulatif']==Data['Produksi Kumulatif'].max()]
     bar_chart = px.bar(Data, x='Tahun',y='Produksi')
     st.plotly_chart(bar_chart,use_container_width=True)
     st.subheader("Produksi minyak paling tinggi secara kumulatif:")
     st.dataframe(total)

     st.subheader("Produksi minyak paling rendah:")
     Data = dataset[dataset['Produksi'] != 0]
     Data = Data[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     total = Data[Data['Produksi']==Data['Produksi'].min()]
     st.dataframe(total)

     Data = dataset[dataset['Produksi'] == 0]
     st.subheader("Negara-negara yang tidak berproduksi:")
     total = Data[['Negara','Tahun','Produksi','Kode','country-code','region','sub-region']]
     st.dataframe(total)

     

     
st.sidebar.subheader("Analisa data berdasarkan negara")
datanegara = pd.read_json('kode_negara_lengkap.json')
pilihanNegara = st.sidebar.selectbox('Pilih negara',datanegara['name'])
state_data = dataset[dataset['Negara'] == pilihanNegara]

def get_total_dataframe(dataset):
    total_dataframe = dataset[['Negara','Tahun','Produksi']]
    return total_dataframe
def get_data_info(dataset):
    info_data = dataset[['Negara','Kode','country-code','region','sub-region','Tahun','Produksi']]
    pd.set_option('display.max_colwidth', 0)
    return info_data

state_total = get_total_dataframe(state_data)
if st.sidebar.checkbox("Lihat Negara"):
     st.header("Analisa data Negara")
     st.subheader("Tampilan data negara: "+pilihanNegara)
     st.write(state_total,width=2024, height=2000)

     if st.sidebar.checkbox("Lihat grafik"):
          st.subheader("Tampilan grafik pada negara: "+pilihanNegara)
          state_total_graph = px.bar(state_total, x='Tahun',y='Produksi',labels=("Negara penghasil minyak = "+pilihanNegara))
          st.plotly_chart(state_total_graph,use_container_width=True)

          dataMax = state_total.nlargest(10, 'Produksi')
          dataf = dataMax[['Negara','Tahun','Produksi']]
          tahun_hasil = dataMax[dataMax['Produksi']==dataMax['Produksi'].max()]
          tahun_max = tahun_hasil['Tahun']
          tahun_max = tahun_max.to_string(index=False)
          st.subheader(pilihanNegara+" menghasilkan produksi tertinggi pada tahun "+tahun_max)
          if st.sidebar.checkbox("Lihat detail negara produksi "+pilihanNegara):
               st.header("Data untuk Negara "+pilihanNegara)
               info_negara = get_data_info(state_data)
               st.write(info_negara)
            

#Analisa data berdasarkan tahun
st.sidebar.subheader("Analisa data berdasarkan tahun")
pilihanTahun = st.sidebar.selectbox('Pilih Tahun',dataset['Tahun'])
tahun = dataset[dataset['Tahun'] == pilihanTahun]

def get_total_year(dataset):
    tahun =dataset[dataset["Tahun"] == pilihanTahun]
    year_dataframe = tahun[['Negara','Tahun','Produksi']]
    return year_dataframe
year_total = get_total_year(tahun)

if st.sidebar.checkbox("Lihat Tahun"):
     dataset_bersih = dataset[dataset['Produksi'] != 0]
     dataset_tahun = dataset_bersih[['Negara','Tahun','Produksi','Kode','region','sub-region']]  
     st.header("Analisa data berdasarkan Tahun")
     if st.sidebar.checkbox("Grafik berdasar tahun"):
          st.subheader("Data negara penghasil pada tahun "+str(pilihanTahun))
          year_total_graph = px.bar(year_total,x='Produksi',y='Negara',labels={'Jumlah':'Produksi tahun %s' % (pilihanTahun)})
          st.plotly_chart(year_total_graph,use_container_width=True)
          if st.sidebar.checkbox("Lihat 5 produsen tertinggi %s"%(pilihanTahun)):
               st.subheader("5 Negara produsen tertinggi pada tahun "+str(pilihanTahun))
               data_5 = year_total.nlargest(5, 'Produksi')
               data_hasil = data_5[['Negara','Tahun','Produksi']]
               max_data = px.bar(data_hasil, x='Produksi',y='Negara',labels={'Jumlah':'Produksi tahun %s' % (pilihanTahun)})
               st.plotly_chart(max_data,use_container_width=True)
               tahun_hasil = data_5[data_5['Produksi']==data_5['Produksi'].max()]
               negara_max = tahun_hasil['Negara']
               negara_max = negara_max.to_string(index=False)
               st.subheader(negara_max+" menjadi negara penghasil minyak tertinggi pada tahun "+str(pilihanTahun))
     if st.sidebar.checkbox("Informasi data berdasar tahun"):
          st.markdown("Produksi paling tinggi %s"%(pilihanTahun))
          data_tahun =dataset_tahun[dataset_tahun["Tahun"] == pilihanTahun]
          data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].max()]
          st.write(data_tahun)

          st.markdown("Produksi paling rendah %s"%(pilihanTahun))
          data_rendah =dataset_tahun[dataset_tahun["Tahun"] == pilihanTahun]
          data_rendah=data_rendah[data_rendah['Produksi']==data_rendah['Produksi'].min()]
          st.write(data_rendah)

          st.markdown("Negara tidak produksi pada tahun %s"%(pilihanTahun))
          tidak_produksi = dataset[dataset["Tahun"] == pilihanTahun]
          tidak_produksi = tidak_produksi[tidak_produksi['Produksi'] == 0]
          tidak_produksi = tidak_produksi[['Negara','Tahun','Produksi','Kode','region','sub-region']]
          st.write(tidak_produksi)





          
