from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User,auth 
from django.contrib import messages
from .models import Insurance_Claim
# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method=="POST":
        first=request.POST['fname']
        last=request.POST['lname']
        uname=request.POST['uname']
        em=request.POST['email']
        ps=request.POST['psw']
        ps1=request.POST['psw1']
        if ps==ps1:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"Username Exists")
                return render(request,"register.html")
            elif User.objects.filter(email=em).exists():
                messages.info(request,"Email exists")
                return render(request,"register.html")
            else:
                user=User.objects.create_user(first_name=first,
            last_name=last,username=uname,email=em,password=ps)
                user.save()
                return HttpResponseRedirect("login")
        else:
            messages.info(request,"Password not Matching")
            return render(request,"register.html")

    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        ps=request.POST['psw']
        user=auth.authenticate(username=uname,password=ps)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('data')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request,"login.html")

def adminlogin(request):
    if request.method=="POST":
        un=request.POST['uname']
        ps=request.POST['psw']
        user=auth.authenticate(username=un,password=ps)
        if user.is_superuser is not None:
            auth.login(request,user)
            return HttpResponseRedirect('adminhome')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"adminlogin.html")
    return render(request,"adminlogin.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def data(request):
    if request.method=="POST":
        age=int(request.POST['age'])
        gender=request.POST['gender']
        edu=request.POST['education']
        occu=request.POST['occupation']
        rel=request.POST['rel']
        inci=request.POST['type']
        colli=request.POST['collision']
        sev=request.POST['severity']
        authorities=request.POST['authorities']
        veh=int(request.POST['vehicle'])
        prop=request.POST['property']
        inju=int(request.POST['injuries'])
        wit=int(request.POST['witness'])
        pol=request.POST['police']
        tot_claim=int(request.POST['tot_claim'])
        inju_claim=int(request.POST['injury'])
        prop_claim=int(request.POST['property_claim'])
        veh_claim=int(request.POST['vehclaim'])
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        gender1=l.fit_transform([gender])
        edu1=l.fit_transform([edu])
        occu1=l.fit_transform([occu])
        rel1=l.fit_transform([rel])
        inci1=l.fit_transform([inci])
        colli1=l.fit_transform([colli])
        sev1=l.fit_transform([sev])
        authorities1=l.fit_transform([authorities])
        prop1=l.fit_transform([prop])
        pol1=l.fit_transform([pol])

        import pandas as pd
        df=pd.read_csv(r"static/dataset/Insuranceclaim.csv")
        print(df.head())
        df['collision_type']=df['collision_type'].replace(to_replace="?",value="Rear Collision")
        df['property_damage']=df['property_damage'].replace(to_replace="?",value="YES")
        df['police_report_available']=df['police_report_available'].replace(to_replace="?",value="YES")
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        sex_num=l.fit_transform(df['insured_sex'])
        edu_num=l.fit_transform(df['insured_education_level'])
        occu_num=l.fit_transform(df['insured_occupation'])
        rel_num=l.fit_transform(df['insured_relationship'])
        inci_num=l.fit_transform(df['incident_type'])
        colli_num=l.fit_transform(df['collision_type'])
        sev_num=l.fit_transform(df['incident_severity'])
        prop_num=l.fit_transform(df['property_damage'])
        pol_num=l.fit_transform(df['police_report_available'])
        auth_num=l.fit_transform(df["authorities_contacted"])
        df=df.drop(["insured_sex","insured_education_level","insured_occupation",
            "insured_hobbies","insured_relationship","incident_type",
            "collision_type","incident_severity","authorities_contacted","property_damage","police_report_available"],axis=1)
        df["Gender"]=sex_num
        df["Insured_Education"]=edu_num
        df["Insured_Occupation"]=occu_num
        df["Insured_Relationship"]=rel_num
        df["Incident_Type"]=inci_num
        df["Collision_Type"]=colli_num
        df["Incident_Severity"]=sev_num
        df["Property_Damage"]=prop_claim
        df["Police_Report_Available"]=pol_num
        df["Authorities_Contacted"]=auth_num
        df=df.drop("incident_hour_of_the_day",axis=1)
        print(df.head())
        X=df.drop("fraud_reported",axis=1)
        y=df["fraud_reported"]
        from sklearn.model_selection import train_test_split
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.34)
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
        log=LogisticRegression()
        log.fit(X_train,y_train)
        pred_log=log.predict(X_test)
        from sklearn.naive_bayes import GaussianNB
        gb=GaussianNB()
        gb.fit(X_train,y_train)
        pred_gb=gb.predict(X_test)
        from sklearn.neighbors import KNeighborsClassifier
        knn=KNeighborsClassifier()
        knn.fit(X_train,y_train)
        pred_knn=knn.predict(X_test)
        from sklearn.svm import SVC
        svc=SVC()
        svc.fit(X_train,y_train)
        pred_svc=svc.predict(X_test)
        from sklearn.ensemble import RandomForestClassifier
        rfc=RandomForestClassifier()
        rfc.fit(X_train,y_train)
        pred_rfc=rfc.predict(X_test)
        print("Logistic Regression: ",accuracy_score(pred_log,y_test))
        print("Gaussian Naive Bayes: ",accuracy_score(pred_gb,y_test))
        print("SVM: ",accuracy_score(pred_svc,y_test))
        print("Random Forest: ",accuracy_score(pred_rfc,y_test))
        print("KNN: ",accuracy_score(pred_knn,y_test))
        from sklearn.svm import SVC
        rfc=SVC()
        rfc.fit(X,y)
        import numpy as np
        pred_data=np.array([[age,gender1,edu1,occu1,rel1,inci1,
        colli1,sev1,authorities1,veh,prop1,inju,
        wit,pol1,tot_claim,inju_claim,prop_claim,veh_claim]],dtype=object)
        prediction=rfc.predict(pred_data)
        print(prediction)
        ic=Insurance_Claim.objects.create(Age=age,Gender=gender,Education=edu,Occupation=occu,Relationship=rel,
        Incident_Type=inci,Collision_Type=colli,Incident_Severity=sev,Authorities_Contacted=authorities,
        Vehicle_Damage=veh,Property_Damage=prop,Bodily_Injuries=inju,Witness=wit,
        Police_Report=pol,Total_Claim=tot_claim,Injury_Claim=inju_claim,
        Property_Claim=prop_claim,Vehicle_Claim=veh_claim,Prediction=prediction)
        ic.save()
        return render(request,"predict.html",{"age":age,"gender":gender,
        "education":edu,"occupation":occu,"relationship":rel,
        "incident":inci,"collision":colli,"severity":sev,
        "auth":authorities,"veh":veh,"property":prop,
        "injuries":inju,"witness":wit,"police":pol,
        "tot_claim":tot_claim,"inju_claim":inju_claim,
        "prop_claim":prop_claim,"veh_claim":veh_claim,
        "prediction":prediction
        })

    return render(request,"data.html")


def predict(request):
    return render(request,"predict.html")


def adminhome(request):
    ic=Insurance_Claim.objects.all()
    return render(request,"adminhome.html",{"ic":ic})
