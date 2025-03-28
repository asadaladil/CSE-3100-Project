import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random
Country1=['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 
         'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 
         'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 
         'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 
         'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Congo-Brazzaville)', 
         'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia (Czech Republic)', 'Denmark', 'Djibouti', 'Dominica', 
         'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 
         'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 
         'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 
         'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 
         'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 
         'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 
         'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 
         'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 
         'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 
         'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 
         'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 
         'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 
         'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 
         'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 
         'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 
         'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 
         'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 
         'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']


Bd_city=(('Rajshahi','Rajshahi'),
                  ('Dhaka','Rajshahi'),
                  ('Khulna','Khulna'),
                  ('Sylhet','Sylhet'),
                  ('Barisal','Barisal'),
                  ('Rangpur','Rangpur'),
                  ('Chittagong','Chittagong')
                  )
idd='1'
def make_city():
    city={}
    for i in Country1:
        city[i]=()
    city["Bangladesh"]=Bd_city
    return city
Type=(('Cost','Cost'),('Income','Income'))

acnt=2131000000
Description=(
    ('Check Deposit','Check Deposit'),
    ('Cash Deposit','Cash Deposit'),
    ('Cash Withdraw','Cash Withdraw'),
    ('Cash Income','Cash Income'),
    ('Cash Expense','Cash Expense')
    
)
def country():
    global Country1
    Country2=[]
    for i in Country1:
        Country2.append((i,i))
    return tuple(Country2)

def BarGraph(List,total,nm):
    categories = []
    values = []
    for i in List:
        categories.append(i[0])
        values.append((i[1]/total)*100)
    bars=plt.bar(categories, values, color='skyblue')
    plt.title(f"{nm} Graph")
    plt.xlabel('Categories')
    plt.ylabel('Percentages(%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, 
            f'{round(height,2)}%', ha='center', va='bottom')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return image_base64

def PieGraph(income,cost):
    labels = ['Savings','Cost']
    s=round((income-cost)/income*100,2)
    c=round(cost/income*100,2)
    sizes = [s,c]
    colors = ['lightgreen','lightcoral']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  
    plt.title('Basic Pie Chart (Matplotlib)')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return image_base64

   
# A=BarGraph([["Get Fund", 100], ["Script Evaluate", 6100]],6200,'Income')
# PieGraph(6100,2000)

def make_otp():
    num=random.randint(100000,999999)
    return str(num)