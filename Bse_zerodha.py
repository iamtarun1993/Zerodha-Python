import pandas as pd
import urllib
import zipfile
import datetime
import webbrowser
from datetime import timedelta
pd.set_option('display.expand_frame_repr', False)

def download_zip(filename,url):
	print "Downloading zip file from BSE.."
	urllib.urlretrieve(url, filename+".zip");
	unzip_file_zip(filename)

def unzip_file_zip(filename):
	zip_ref = zipfile.ZipFile(filename+'.zip', 'r')
	zip_ref.extractall();
	zip_ref.close();
	csv_data_read(filename)

def csv_data_read(filename):
	url=filename+".CSV"
	data_csv_frame = pd.read_csv(url);
	data_csv_frame.drop(['TDCLOINDI','NET_TURNOV','NO_OF_SHRS','NO_TRADES','PREVCLOSE','SC_GROUP','SC_TYPE','LAST'], axis = 1, inplace = True)
	#print(data_csv_frame);
	data_csv_frame['CHANGE_PER'] = ((data_csv_frame.CLOSE - data_csv_frame.OPEN)/data_csv_frame.OPEN)*100;
	print("\nTop 10 Profit Stocks are :")
	top_10_profit_stock=data_csv_frame.nlargest(10, 'CHANGE_PER');
	top_10_profit_stock.drop(['OPEN','CLOSE','LOW','HIGH'], axis = 1, inplace = True)
	print top_10_profit_stock;
	print("\nTop 10 Loss Stocks are :")
	top_10_loss_stock=data_csv_frame.nsmallest(10, 'CHANGE_PER');
	top_10_loss_stock.drop(['OPEN','CLOSE','LOW','HIGH'], axis = 1, inplace = True)
	print top_10_loss_stock;
	#find_stock_info(data_csv_frame);

def find_stock_info(data_csv_frame):
	stock_code=input("Enter 6 digit Stock Code: ");
	stock_full_info=data_csv_frame[data_csv_frame["SC_CODE"] == stock_code];
	print(stock_full_info);
	# f = open('topstock.html','w')
	# f.write("""<html>
	# <head></head>
	# <body><table><tbody>""")
	# for i in range(0, len(top_10_profit_stock)):
	# 	f.write("<tr><td>"+str(top_10_profit_stock.iloc[i]['SC_NAME'])+"</td></tr>")
	
	# f.write("""</tbody></table></body>
	# </html>""")
	# f.close()

	# webbrowser.open_new_tab('topstock.html')

def file_date_avail(newday):
	# print(str(newday.year).zfill(2));
	# print (newday.strftime("%y"))
	filename='EQ'+str(newday.day).zfill(2)+str(newday.month).zfill(2)+str(newday.strftime("%y"))
	#print(filename)
	#filename='EQ300418'
	url = 'https://www.bseindia.com/download/BhavCopy/Equity/'+filename+'_CSV.ZIP'
	ret = urllib.urlopen(url)
	if (ret.code == 200):
		print("File Found for "+str(newday.strftime('%d/%m/%Y')));
		download_zip(filename,url);
	else:
		print("No file found for "+str(newday.strftime('%d/%m/%Y')));
		newday=newday-timedelta(1);
		file_date_avail(newday);


def main():
	today = datetime.datetime.now()
	#print(today);
	file_date_avail(today);
	




if __name__== "__main__":
  main();

