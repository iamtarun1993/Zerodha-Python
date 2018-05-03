import pandas as pd
import urllib
import zipfile
import datetime
from datetime import timedelta
pd.set_option('display.expand_frame_repr', False)

def download_zip(filename,url):
	print "Downloading zip file from BSE.."
	urllib.urlretrieve(url, filename+".zip");
	unzip_file_zip(filename)

def unzip_file_zip(filename):
	zip_ref = zipfile.ZipFile(filename+'.zip', 'r')
	zip_ref.extractall()
	zip_ref.close()
	csv_data_read(filename)

def csv_data_read(filename):
	url=filename+".CSV"
	data_csv_frame = pd.read_csv(url);
	data_csv_frame.drop(['TDCLOINDI','NET_TURNOV','NO_OF_SHRS','NO_TRADES','PREVCLOSE','SC_GROUP','SC_TYPE','LAST'], axis = 1, inplace = True)
	print(data_csv_frame);

def file_date_avail(newday):
	# print(str(newday.year).zfill(2));
	# print (newday.strftime("%y"))
	filename='EQ'+str(newday.day).zfill(2)+str(newday.month).zfill(2)+str(newday.strftime("%y"))
	print(filename)
	#filename='EQ300418'
	url = 'https://www.bseindia.com/download/BhavCopy/Equity/'+filename+'_CSV.ZIP'
	ret = urllib.urlopen(url)
	if (ret.code == 200):
		print("File Found for "+str(newday));
		download_zip(filename,url);
	else:
		print("No file found for "+str(newday));
		newday=newday-timedelta(1);
		file_date_avail(newday);


def main():
	today = datetime.datetime.now()
	print(today);
	file_date_avail(today);
	




if __name__== "__main__":
  main();
