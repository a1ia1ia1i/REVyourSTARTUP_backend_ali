from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .dataparse import *
from .yearformparse import *


class HealthCheckAPIView(APIView):
    def get(self, request):
        response = {'Message': "Hello, Yibran"}
        return Response(response, status=status.HTTP_200_OK)
    

class MakeSuperUserView(APIView):
    # This should only be used to make yourself a superuser in order to access the /admin functionality
    def put(self, request):
        username = request.data.get("username")
        user = User.objects.get(username=username)

        if user:
            user.is_superuser = 1
            user.is_staff = 1
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)

class RegisterNewUserView(APIView):
    # Simple registration view using Djangos built-in User class
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")


        user = User.objects.create_user(username, email, password)

        response = {'User_ID': user.id, 'Username': user.username, 'Email': user.email}
        return Response(response, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    # Simple authentication view using Djangos built-in User class and authentication() function

    # TODO: Should include some kind of tokenization in order to keep track of users session
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Backend authenticated credentials
            if user.is_active:
                login(request, user)
                
                return Response({"userID": user.id}, status=status.HTTP_202_ACCEPTED)
            else:
                message = "User is inactive"
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Credentials were not authenticated
            message = "Unable to authenticate user"
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    # Simple Logout View
    # TODO: This should be finished once there is some functionality associated with cookies, session, etc..
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ListAllUsersView(ListAPIView):
    # Generic View for listing all users in the database
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetUserByIDView(APIView):
    # View demonstrating how to use a serializer to get a user by their id
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


#class CreateMainFormView(APIView):
    # View which allows the main form to be created and linked to a user's id
    # JSON
    # {
    #   'user_id': 1,
    #   'form_name': 'Sample Form Name'
    # }

    # def post(self, request):
    #     user_id = request.data.get('user_id')
    #     form_name = request.data.get("form_name")
    #     user = get_object_or_404(User, id=user_id)
    #     if form_name:
    #         serializer = MainFormSerializer(data={'user': user.id, 'form_name': form_name})
    #     else:
    #         serializer = MainFormSerializer(data={'user': user.id})

    #     if serializer.is_valid():
    #         serializer.save()
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetMainFormByUserView(APIView):
    # View should be passed the User's id in the endpoint link, it will search for all the 
    # MainForm's associated with that id, and return a list of all the MainForm objects corresponding
    # to that specific User

    def get(self, request, id):
        try:
            queryset = MainForm.objects.filter(user_id=id)
            serializer = MainFormSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except MainForm.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)
        
    # The post request should contain the User's id in the enpoint link, and also have the "form_name"
    # sent as a JSON, otherwise the response will be an error
    def post(self, request, id):
        form_name = request.data.get("form_name")
        user = get_object_or_404(User, id=id)
        if form_name:
            serializer = MainFormSerializer(data={'user': user.id, 'form_name': form_name})
        else:
            error = "Error: field 'form_name' missing from request"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RevFormView(APIView):
    # This view should handle the rev form in terms of GET, POST, PUT, and adhere to the JSON format
    # given in dataStructure_RevForm.json

    def post(self, request, mainform_id):
        # Parse the JSON starting with the outer-most tags
        valuation_data = request.data.get('valuationParameters')
        reality_check = request.data.get('realityCheck1')
        customer_segments_year3 = request.data.get('customerSegmentsYear3')
        customer_segments_year2 = request.data.get('customerSegmentsYear2')
        customer_segments_year1 = request.data.get('customerSegmentsYear1')

        if valuation_data is None or reality_check is None or customer_segments_year3 is None or customer_segments_year2 is None or customer_segments_year1 is None:
            # If either of these tags are missing, create an error and return a BAD_REQUEST Response
            error = 'Invalid request: Data is either mislabeled or missing entirely'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Otherwise parse through the nested tags and create a serializer object for database 
            # storage. Also, should check for the validation of the data being stored

            # This is for testing pusposes only!
            #data_dict = {'valuationParameters': valuation_data, 'realityCheck1': reality_check}

            # This line is for parsing the json data in terms of the outer-most tags
            rev_form_data_dict = flatten_revform_json(valuation_data, reality_check)

            try:
                # Use flattened data_dict to serialize and, if valid, save in the database
                revform_serializer = RevFormSerializer(data=rev_form_data_dict)
                if revform_serializer.is_valid():
                    revform_serializer.save()

                    # Parse through all 3 of the customer_segments, create the appropriate 
                    # rev_form_row_index table, and all the corresponding revform_row tables

                    # YEAR 1
                    data_dict_year1 = flatten_revform_rows_json(customer_segments_year1, 'customerSegmentsYear1')
                    rev_form_rows_index_year1_serializer = RevFormRowsIndexSerializer(data=data_dict_year1['RevFormRowsIndex'])
                    if rev_form_rows_index_year1_serializer.is_valid():                      
                        rev_form_rows_index_year1_serializer.save()
                        rev_form_rows_index_year1_pk = rev_form_rows_index_year1_serializer.data['revform_rows_index_id']
                        RevFormRowsIndex.objects.filter(revform_rows_index_id=rev_form_rows_index_year1_pk).update(rev_form=revform_serializer.data['rev_form_id'])
                    else:
                        return Response(rev_form_rows_index_year1_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    row_data_dict = data_dict_year1['RevFormRows']
                    for key in row_data_dict.keys():
                        rev_form_row_serializer = RevFormRowsSerializer(data=row_data_dict[key])
                        if rev_form_row_serializer.is_valid():
                            rev_form_row_serializer.save()
                            rev_form_row_pk = rev_form_row_serializer.data['revform_rows_id']
                            RevFormRows.objects.filter(revform_rows_id=rev_form_row_pk).update(revform_rows_index=rev_form_rows_index_year1_serializer.data['revform_rows_index_id'])
                        else:
                            error = "Row {} serializer failed to validate".format(key)
                            error_response = {"Message": error, "Serializer": rev_form_row_serializer.errors}
                            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

                    # YEAR 2
                    data_dict_year2 = flatten_revform_rows_json(customer_segments_year2, 'customerSegmentsYear2')
                    rev_form_rows_index_year2_serializer = RevFormRowsIndexSerializer(data=data_dict_year2['RevFormRowsIndex'])
                    if rev_form_rows_index_year2_serializer.is_valid():                      
                        rev_form_rows_index_year2_serializer.save()
                        rev_form_rows_index_year2_pk = rev_form_rows_index_year2_serializer.data['revform_rows_index_id']
                        RevFormRowsIndex.objects.filter(revform_rows_index_id=rev_form_rows_index_year2_pk).update(rev_form=revform_serializer.data['rev_form_id'])
                    else:
                        return Response(rev_form_rows_index_year2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    row_data_dict = data_dict_year2['RevFormRows']
                    for key in row_data_dict.keys():
                        rev_form_row_serializer = RevFormRowsSerializer(data=row_data_dict[key])
                        if rev_form_row_serializer.is_valid():
                            rev_form_row_serializer.save()
                            rev_form_row_pk = rev_form_row_serializer.data['revform_rows_id']
                            RevFormRows.objects.filter(revform_rows_id=rev_form_row_pk).update(revform_rows_index=rev_form_rows_index_year2_serializer.data['revform_rows_index_id'])
                        else:
                            error = "Row {} serializer failed to validate".format(key)
                            error_response = {"Message": error, "Serializer": rev_form_row_serializer.errors}
                            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
                    
                     # YEAR 3
                    data_dict_year3 = flatten_revform_rows_json(customer_segments_year3, 'customerSegmentsYear3')
                    rev_form_rows_index_year3_serializer = RevFormRowsIndexSerializer(data=data_dict_year3['RevFormRowsIndex'])
                    if rev_form_rows_index_year3_serializer.is_valid():                      
                        rev_form_rows_index_year3_serializer.save()
                        rev_form_rows_index_year3_pk = rev_form_rows_index_year3_serializer.data['revform_rows_index_id']
                        RevFormRowsIndex.objects.filter(revform_rows_index_id=rev_form_rows_index_year3_pk).update(rev_form=revform_serializer.data['rev_form_id'])
                    else:
                        return Response(rev_form_rows_index_year3_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    row_data_dict = data_dict_year3['RevFormRows']
                    for key in row_data_dict.keys():
                        rev_form_row_serializer = RevFormRowsSerializer(data=row_data_dict[key])
                        if rev_form_row_serializer.is_valid():
                            rev_form_row_serializer.save()
                            rev_form_row_pk = rev_form_row_serializer.data['revform_rows_id']
                            RevFormRows.objects.filter(revform_rows_id=rev_form_row_pk).update(revform_rows_index=rev_form_rows_index_year3_serializer.data['revform_rows_index_id'])
                        else:
                            error = "Row {} serializer failed to validate".format(key)
                            error_response = {"Message": error, "Serializer": rev_form_row_serializer.errors}
                            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


                    # Update the appropriate MainForm with the newly created RevForm as a foreign key
                    MainForm.objects.filter(main_form_id=mainform_id).update(rev_form=revform_serializer.data['rev_form_id'])
                    return Response(revform_serializer.data, status=status.HTTP_201_CREATED)     
                else:
                    return Response(revform_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except MainForm.DoesNotExist as exception:
                return Response(str(exception), status=status.HTTP_404_NOT_FOUND)
            

    def get(self, request, mainform_id):
        # Get the Main Form and the associated RevForm and RevFormIndex by the given mainform_id
        try:
            mainform = MainForm.objects.get(main_form_id=mainform_id)
            revform = RevForm.objects.get(rev_form_id=mainform.rev_form.rev_form_id)
            revform_index = RevFormRowsIndex.objects.filter(rev_form=revform.rev_form_id)
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the multiple RevFormIndex objects for parsing
        revform_index_serializer = RevFormRowsIndexSerializer(revform_index, many=True)

        # Parse the individual RevFormIndex Objects by their revform_rows_name and populate 
        # new variables with the appropriate data
        for i in range(len(revform_index_serializer.data)):
            if revform_index_serializer.data[i]["revform_rows_name"] == "customerSegmentsYear1":
                customer_segments_year1 = revform_index_serializer.data[i]
            elif revform_index_serializer.data[i]["revform_rows_name"] == "customerSegmentsYear2":
                customer_segments_year2 = revform_index_serializer.data[i]
            elif revform_index_serializer.data[i]["revform_rows_name"] == "customerSegmentsYear3":
                customer_segments_year3 = revform_index_serializer.data[i]

        # Given each RevFormIndex, get all the related RevFormRow objects associated with it,
        # serialize all of them, and then build the segment's "customerSegmentsYearx" json
        try:
            year1_rows = RevFormRows.objects.filter(revform_rows_index=customer_segments_year1["revform_rows_index_id"])
            year1_rows_serializer = RevFormRowsSerializer(year1_rows, many=True)
            year1_customer_segment_json = build_rev_customer_segments_json(customer_segments_year1, year1_rows_serializer.data)
            
            year2_rows = RevFormRows.objects.filter(revform_rows_index=customer_segments_year2["revform_rows_index_id"])
            year2_rows_serializer = RevFormRowsSerializer(year2_rows, many=True)
            year2_customer_segment_json = build_rev_customer_segments_json(customer_segments_year2, year2_rows_serializer.data)
            
            year3_rows = RevFormRows.objects.filter(revform_rows_index=customer_segments_year3["revform_rows_index_id"])        
            year3_rows_serializer = RevFormRowsSerializer(year3_rows, many=True)
            year3_customer_segment_json = build_rev_customer_segments_json(customer_segments_year3, year3_rows_serializer.data)
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)

        # Pass the RevForm, and all the customerSegmentsYearx json's to be built into the correct
        # response format
        built_revform = build_revform_json(revform, year1_customer_segment_json, year2_customer_segment_json, year3_customer_segment_json)
        return Response(built_revform, status=status.HTTP_200_OK)
    

class ProFormaView(APIView):
    def post(self, request, mainform_id):
        pro_forma_startup_factors = request.data.get("proFormaStartupFactors")
        founders_list = pro_forma_startup_factors["foundersDraw"]["founders"]

        if pro_forma_startup_factors is None:
            # If this tag is missing, create an error and return a BAD_REQUEST Response
            error = 'Invalid request: Data is either mislabeled or missing entirely'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            pro_forma_data_dict = flatten_pro_forma_json(pro_forma_startup_factors)

            pro_forma_serializer = ProFormaSerializer(data=pro_forma_data_dict)
            if pro_forma_serializer.is_valid():
                pro_forma_serializer.save()

                num_founders = pro_forma_startup_factors["foundersDraw"]["numberOfFounders"]

                for i in range(num_founders):
                    founders_data_dict = flatten_pro_forma_founders_json(founders_list[i])
                    founders_serializer = ProFormaFoundersSerializer(data=founders_data_dict)
                    if founders_serializer.is_valid():
                        founders_serializer.save()
                        founders_pk = founders_serializer.data['pro_forma_founder_id']
                        ProFormaFounders.objects.filter(pro_forma_founder_id=founders_pk).update(pro_forma=pro_forma_serializer.data['pro_forma_id'])

                    else:
                        return Response(founders_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                MainForm.objects.filter(main_form_id=mainform_id).update(pro_forma=pro_forma_serializer.data['pro_forma_id'])
                
            else:
                return Response(pro_forma_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

        return Response(pro_forma_serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, mainform_id):
        try:
            main_form = MainForm.objects.get(main_form_id = mainform_id)
            pro_forma = ProForma.objects.get(pro_forma_id=main_form.pro_forma.pro_forma_id)
            pro_forma_founders = ProFormaFounders.objects.filter(pro_forma=pro_forma.pro_forma_id)
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)
        
        pro_forma_founders_serializer = ProFormaFoundersSerializer(pro_forma_founders, many=True)
        founders_dict = {"founders": []}
        for i in range(len(pro_forma_founders_serializer.data)):
            founder_json = build_pro_forma_founders_json(pro_forma_founders_serializer.data[i])
            founders_dict['founders'].append(founder_json)

        pro_forma_serializer = ProFormaSerializer(pro_forma)

        built_pro_forma = build_pro_forma_json(pro_forma_serializer.data, founders_dict)

        return Response(built_pro_forma, status=status.HTTP_200_OK)
    


class DepreciationView(APIView):
    def post(self, request, mainform_id):
        depreciation_data = request.data.get("depreciation")

        if depreciation_data is None:
            # If this tag is missing, create an error and return a BAD_REQUEST Response
            error = 'Invalid request: Data is either mislabeled or missing entirely'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            depreciation_schedule = depreciation_data["depreciationSchedule"]
            depreciation_form = flatten_depreciation_form_json(depreciation_data)
            depreciation_form_serializer = DepreciationFormSerializer(data=depreciation_form)
            if depreciation_form_serializer.is_valid():
                depreciation_form_serializer.save()
                depreciation_pk = depreciation_form_serializer.data['depreciation_id']
                for i in range(len(depreciation_schedule)):
                    schedule_entry = {"date": depreciation_schedule[i]["date"], "amount": float(depreciation_schedule[i]["amount"])}
                    depreciation_schedule_serializer = DepreciationScheduleSerializer(data=schedule_entry)
                    if depreciation_schedule_serializer.is_valid():
                        depreciation_schedule_serializer.save()
                        depreciation_schedule_pk = depreciation_schedule_serializer.data['depreciation_schedule_id']
                        DepreciationSchedule.objects.filter(depreciation_schedule_id=depreciation_schedule_pk).update(depreciation_form=depreciation_pk)
                    else:
                        return Response(depreciation_schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                MainForm.objects.filter(main_form_id=mainform_id).update(depreciation_form=depreciation_pk)
            else:
                return Response(depreciation_form_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(depreciation_form_serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request, mainform_id):
        try:
            main_form = MainForm.objects.get(main_form_id = mainform_id)
            depreciation_form = DepreciationForm.objects.get(depreciation_id=main_form.depreciation_form.depreciation_id)
            depreciaiton_schedules = DepreciationSchedule.objects.filter(depreciation_form=depreciation_form.depreciation_id)
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)
        
        depreciation_form_serializer = DepreciationFormSerializer(depreciation_form)
        depreciation_schedule_serializer = DepreciationScheduleSerializer(depreciaiton_schedules, many=True)
        built_depreciation_form = build_depreciation_form_json(depreciation_form_serializer.data, depreciation_schedule_serializer.data)
        return Response(built_depreciation_form, status=status.HTTP_200_OK)
    

class YearFormView(APIView):
    def get(self, request, mainform_id, year_num):
        # Get MainForm and appropriate YearForm
        try:
            main_form = MainForm.objects.get(main_form_id=mainform_id)

            if year_num == 1:
                year_form = YearForm.objects.get(year_form_id=main_form.year1_form.year_form_id)
                main_tag = "year1"
            elif year_num == 2:
                year_form = YearForm.objects.get(year_form_id=main_form.year2_form.year_form_id)
                main_tag = "year2"
            elif year_num == 3:
                year_form = YearForm.objects.get(year_form_id=main_form.year3_form.year_form_id)
                main_tag = "year3"
            else:
                error = "Error: <int:year_num> must be 1, 2, or 3"
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)

        # Get all required tables from the database, serialize them, and build the main json
        try:
            built_json = {main_tag: {}}

            # AdditionalRevenue
            additional_revenue = AdditionalRevenue.objects.get(year_form=year_form.year_form_id)
            additional_revenue_serializer = AdditionalRevenueSerializer(additional_revenue)
            additional_revenue_json = build_additional_revenue_json(additional_revenue_serializer.data)
            built_json[main_tag]['additionalRevenue'] = additional_revenue_json['additionalRevenue']

            # BankingFees
            banking_fees = BankingFees.objects.get(year_form=year_form.year_form_id)
            banking_fees_serializer = BankingFeesSerializer(banking_fees)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name="banking_fees")
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            banking_fees_json = build_banking_fees_json(banking_fees_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['bankingFees'] = banking_fees_json['bankingFees']

            # CashOnHand
            cash_on_hand = CashOnHand.objects.get(year_form=year_form.year_form_id)
            cash_on_hand_serializer = CashOnHandSerializer(cash_on_hand)
            cash_on_hand_json = build_cash_on_hand_json(cash_on_hand_serializer.data)
            built_json[main_tag]['cashOnHand'] = cash_on_hand_json['cashOnHand']

            # CustomerSegments
            customer_segments = CustomerSegments.objects.filter(year_form=year_form.year_form_id)
            customer_segments_serializer = CustomerSegmentsSerializer(customer_segments, many=True)
            segments = []
            for i in range(len(customer_segments_serializer.data)):
                segment_id = customer_segments_serializer.data[i]['customer_segment_id']
                monthly_data = MonthlyData.objects.filter(customer_segment_id=segment_id)
                monthly_data_serializer = MonthlyDataSerializer(monthly_data, many=True)
                segments.append({'segment': customer_segments_serializer.data[i], 'monthly_data': monthly_data_serializer.data})
            customer_segments_json = build_customer_segments_json(segments)
            built_json[main_tag]['customerSegments'] = customer_segments_json['customerSegments']

            # Distributions
            distributions = Distributions.objects.get(year_form=year_form.year_form_id)
            distributions_serializer = DistributionsSerializer(distributions)
            distributions_json = build_distributions_json(distributions_serializer.data)
            built_json[main_tag]['distributions'] = distributions_json['distributions']

            # FixedAssets
            fixed_assets = FixedAssets.objects.get(year_form=year_form.year_form_id)
            fixed_assets_serializer = FixedAssetsSerializer(fixed_assets)
            fixed_assets_json = build_fixed_assets_json(fixed_assets_serializer.data)
            built_json[main_tag]['fixedAssets'] = fixed_assets_json['fixedAssets']

            # FoundersDraw
            founders_draw = FoundersDraw.objects.get(year_form=year_form.year_form_id)
            founders_draw_serializer = FoundersDrawSerializer(founders_draw)
            founders_draw_pay = FoundersDrawPay.objects.filter(founders_draw=founders_draw.founders_draw_id)
            founders_draw_pay_serializer = FoundersDrawPaySerializer(founders_draw_pay, many=True)
            founders_draw_json = build_founders_draw_json(founders_draw_serializer.data, founders_draw_pay_serializer.data)
            built_json[main_tag]['foundersDraw'] = founders_draw_json['foundersDraw']

            # FullTimeWorkers
            full_time_workers = FullTimeWorkers.objects.get(year_form=year_form.year_form_id)
            full_time_workers_serializer = FullTimeWorkersSerializer(full_time_workers)
            workers_list = WorkersList.objects.filter(year_form=year_form.year_form_id, tag_name='full_time_workers')
            workers_list_serializer = WorkersListSerializer(workers_list, many=True)
            full_time_workers_json = build_full_time_workers_json(full_time_workers_serializer.data, workers_list_serializer.data)
            built_json[main_tag]['fullTimeWorkers'] = full_time_workers_json['fullTimeWorkers']

            # FundingInvestment
            funding_investment = FundingInvestment.objects.get(year_form=year_form.year_form_id)
            funding_investment_serializer = FundingInvestmentSerializer(funding_investment)
            funding_investment_json = build_funding_investment_json(funding_investment_serializer.data)
            built_json[main_tag]['fundingInvestment'] = funding_investment_json['fundingInvestment']

            # LegalAndProfessionalServices
            legal_and_professional_services = LegalAndProfessionalServices.objects.get(year_form=year_form.year_form_id)
            legal_and_professional_services_serializer = LegalAndProfessionalServicesSerializer(legal_and_professional_services)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='legal_and_professional_services')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            legal_and_professional_services_json = build_legal_and_professional_services_json(legal_and_professional_services_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['legalAndProfessionalServices'] = legal_and_professional_services_json['legalAndProfessionalServices']

            # MarketingExpenses
            marketing_expenses = MarketingExpenses.objects.get(year_form=year_form.year_form_id)
            marketing_expenses_serializer = MarketingExpensesSerializer(marketing_expenses)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='marketing_expenses')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            marketing_expenses_json = build_marketing_expenses_json(marketing_expenses_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['marketingExpenses'] = marketing_expenses_json['marketingExpenses']

            # OfficeGeneralBusiness
            office_general_business = OfficeGeneralBusiness.objects.get(year_form=year_form.year_form_id)
            office_general_business_serializer = OfficeGeneralBusinessSerializer(office_general_business)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='office_general_business')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            office_general_business_json = build_office_general_business_json(office_general_business_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['officeGeneralBusiness'] = office_general_business_json['officeGeneralBusiness']

            # OtherExpenses
            other_expenses = OtherExpenses.objects.get(year_form=year_form.year_form_id)
            other_expenses_serializer = OtherExpensesSerializer(other_expenses)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='other_expenses')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            other_expenses_json = build_other_expenses_json(other_expenses_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['otherExpenses'] = other_expenses_json['otherExpenses']

            # PartTimeWorkers
            part_time_workers = PartTimeWorkers.objects.get(year_form=year_form.year_form_id)
            part_time_workers_serializer = PartTimeWorkersSerializer(part_time_workers)
            workers_list = WorkersList.objects.filter(year_form=year_form.year_form_id, tag_name='part_time_workers')
            workers_list_serializer = WorkersListSerializer(workers_list, many=True)
            part_time_workers_json = build_part_time_workers_json(part_time_workers_serializer.data, workers_list_serializer.data)
            built_json[main_tag]['partTimeWorkers'] = part_time_workers_json['partTimeWorkers']

            # PayRollTaxesAndBenefits
            pay_roll_taxes_and_benefits = PayRollTaxesAndBenefits.objects.get(year_form=year_form.year_form_id)
            pay_roll_taxes_and_benefits_serializer = PayRollTaxesAndBenefitsSerializer(pay_roll_taxes_and_benefits)
            pay_roll_list = PayRollList.objects.filter(pay_roll_taxes_and_benefits=pay_roll_taxes_and_benefits.pay_roll_tax_and_benefits_id)
            pay_roll_list_serializer = PayRollListSerializer(pay_roll_list, many=True)
            pay_roll_taxes_and_benefits_json = build_pay_roll_taxes_and_benefits_json(pay_roll_taxes_and_benefits_serializer.data, pay_roll_list_serializer.data)
            built_json[main_tag]['payRollTaxesAndBenefits'] = pay_roll_taxes_and_benefits_json['payRollTaxesAndBenefits']

            # ProductionRelated
            production_related = ProductionRelated.objects.filter(year_form=year_form.year_form_id)
            production_related_serializer = ProductionRelatedSerializer(production_related, many=True)
            entries = []
            for i in range(len(production_related_serializer.data)):
                production_related_expense = ProductionRelatedExpense.objects.filter(production_related=production_related_serializer.data[i]['production_related_id'])
                production_related_expense_serializer = ProductionRelatedExpenseSerializer(production_related_expense, many=True)
                entries.append({"production_related": production_related_serializer.data[i], "expenses_list": production_related_expense_serializer.data})
            production_related_json = build_production_related_json(entries)
            built_json[main_tag]['productionRelated'] = production_related_json['productionRelated']

            # PropertyRelated
            property_related = PropertyRelated.objects.get(year_form=year_form.year_form_id)
            property_related_serializer = PropertyRelatedSerializer(property_related)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='property_related')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            property_related_json = build_property_related_json(property_related_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['propertyRelated'] = property_related_json['propertyRelated']

            # ReturnReworks
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='return_reworks')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            return_reworks_json = build_return_reworks_json(expenses_list_serializer.data)
            built_json[main_tag]['returnReworks'] = return_reworks_json['returnReworks']

            # SalariedWorkers
            salaried_workers = SalariedWorkers.objects.get(year_form=year_form.year_form_id)
            salaried_workers_serializer = SalariedWorkersSerializer(salaried_workers)
            workers_list = WorkersList.objects.filter(year_form=year_form.year_form_id, tag_name='salaried_workers')
            workers_list_serializer = WorkersListSerializer(workers_list, many=True)
            salaried_workers_json = build_salaried_workers_json(salaried_workers_serializer.data, workers_list_serializer.data)
            built_json[main_tag]['salariedWorkers'] = salaried_workers_json['salariedWorkers']

            # TravelVehicleRelated
            travel_vehicle_related = TravelVehicleRelated.objects.get(year_form=year_form.year_form_id)
            travel_vehicle_related_serializer = TravelVehicleRelatedSerializer(travel_vehicle_related)
            expenses_list = ExpensesList.objects.filter(year_form=year_form.year_form_id, tag_name='travel_vehicle_related')
            expenses_list_serializer = ExpensesListSerializer(expenses_list, many=True)
            travel_vehicle_related_json = build_travel_vehicle_related_json(travel_vehicle_related_serializer.data, expenses_list_serializer.data)
            built_json[main_tag]['travelVehicleRelated'] = travel_vehicle_related_json['travelVehicleRelated']

            # WorkersHeadCount
            workers_head_count = WorkersHeadCount.objects.get(year_form=year_form.year_form_id)
            workers_head_count_serializer = WorkersHeadCountSerializer(workers_head_count)
            workers_head_count_json = build_workers_head_count_json(workers_head_count_serializer.data)
            built_json[main_tag]['workersHeadCount'] = workers_head_count_json['workersHeadCount']

        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)


        return Response(built_json, status=status.HTTP_200_OK)


    def post(self, request, mainform_id, year_num):
        if year_num == 1:
            main_tag = "year1"
        elif year_num == 2:
            main_tag = "year2"
        elif year_num == 3:
            main_tag = "year3"
        else:
            error = "Error: <int:year_num> must be 1, 2, or 3"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # Get data by the main tag of the json
        year_form_data = request.data.get(main_tag)
        if year_form_data is None:
            error = 'Invalid request: Data is either mislabeled or missing entirely'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            year_form_serializer = YearFormSerializer(data={"which_year": year_num})
            if year_form_serializer.is_valid():
                year_form_serializer.save()
                year_form_pk = year_form_serializer.data['year_form_id']
                if year_num == 1:
                    MainForm.objects.filter(main_form_id=mainform_id).update(year1_form=year_form_pk)
                elif year_num == 2:
                    MainForm.objects.filter(main_form_id=mainform_id).update(year2_form=year_form_pk)
                elif year_num == 3:
                    MainForm.objects.filter(main_form_id=mainform_id).update(year3_form=year_form_pk)
            else:
                return Response(year_form_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Assemble all the relevant tags from the year_form_data according to the model design

        # Process each _data tag and flatten for serialization
        additional_revenue = flatten_additional_revenue_data(year_form_data["additionalRevenue"])
        banking_fees = flatten_banking_fees_data(year_form_data["bankingFees"])
        cash_on_hand = flatten_cash_on_hand_data(year_form_data["cashOnHand"])
        customer_segments = flatten_customer_segments_data(year_form_data["customerSegments"])
        distributions = flatten_distributions_data(year_form_data["distributions"])
        fixed_assets = flatten_fixed_assets_data(year_form_data["fixedAssets"])
        founders_draw = flatten_founders_draw_data(year_form_data["foundersDraw"])
        full_time_workers = flatten_full_time_workers_data(year_form_data["fullTimeWorkers"])
        funding_investment = flatten_funding_investment_data(year_form_data["fundingInvestment"])
        legal_and_professional_services = flatten_legal_and_profesisonal_services_data(year_form_data["legalAndProfessionalServices"])
        marketing_expenses = flatten_marketing_expenses_data(year_form_data["marketingExpenses"])
        office_general_business = flatten_office_general_business_data(year_form_data["officeGeneralBusiness"])
        other_expenses = flatten_other_expenses_data(year_form_data["otherExpenses"])
        part_time_workers = flatten_part_time_workers_data(year_form_data["partTimeWorkers"])
        pay_roll_taxes_and_benefits = flatten_pay_roll_taxes_and_benefits_data(year_form_data["payRollTaxesAndBenefits"])
        # ProductionRelated is Foreign Key'd by another sub-table
        production_related = flatten_production_related_data(year_form_data["productionRelated"])
        property_related = flatten_property_related_data(year_form_data["propertyRelated"])
        # Return Reworks does not have its own model
        return_reworks = flatten_return_reworks_data(year_form_data["returnReworks"])
        salaried_workers = flatten_salaried_workers_data(year_form_data["salariedWorkers"])
        travel_vehicle_related = flatten_travel_vehicle_related_data(year_form_data["travelVehicleRelated"])
        workers_head_count = flatten_workers_head_count_data(year_form_data["workersHeadCount"])

        # Serialize each tag and insert into database (Doing this in reverse order for the sake of testing)

        # Workers Head Count
        workers_head_count_serializer = WorkersHeadCountSerializer(data=workers_head_count)
        if workers_head_count_serializer.is_valid():
            workers_head_count_serializer.save()
            workers_head_count_pk = workers_head_count_serializer.data['workers_head_count_id']
            WorkersHeadCount.objects.filter(workers_head_count_id=workers_head_count_pk).update(year_form=year_form_pk)
        else:
            return Response(workers_head_count_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Travel Vehicle Related
        expenses_list = travel_vehicle_related.pop('expenses_list')
        travel_vehicle_related_serializer = TravelVehicleRelatedSerializer(data=travel_vehicle_related)
        if travel_vehicle_related_serializer.is_valid():
            travel_vehicle_related_serializer.save()
            travel_vehicle_related_pk = travel_vehicle_related_serializer.data['travel_vehicle_related_id']
            TravelVehicleRelated.objects.filter(travel_vehicle_related_id=travel_vehicle_related_pk).update(year_form=year_form_pk)
            for i in range(len(expenses_list)):
                expenses_list_serializer = ExpensesListSerializer(data=expenses_list[i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            name = "travel_vehicle_related"
            errors = travel_vehicle_related_serializer.errors
            return Response({"Serializer": name, "error": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Salaried Workers
        workers_list = salaried_workers.pop('workers_list')
        salaried_workers_serializer = SalariedWorkersSerializer(data=salaried_workers)
        if salaried_workers_serializer.is_valid():
            salaried_workers_serializer.save()
            salaried_workers_pk = salaried_workers_serializer.data['salaried_workers_id']
            SalariedWorkers.objects.filter(salaried_workers_id=salaried_workers_pk).update(year_form=year_form_pk)
            for i in range(len(workers_list)):
                workers_list_serializer = WorkersListSerializer(data=workers_list[i])
                if workers_list_serializer.is_valid():
                    workers_list_serializer.save()
                    workers_list_pk = workers_list_serializer.data['workers_list_id']
                    WorkersList.objects.filter(workers_list_id=workers_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(workers_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            name = "salaried_workers"
            errors = salaried_workers_serializer.errors
            return Response({"Serializer": name, "error": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Return Reworks
        for i in range(len(return_reworks)):
            expenses_list_serializer = ExpensesListSerializer(data=return_reworks[i])
            if expenses_list_serializer.is_valid():
                expenses_list_serializer.save()
                expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
            else:
                name = "return_reworks"
                errors = expenses_list_serializer.errors
                return Response({"Serializer": name, "error": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Property Related
        expenses_list = property_related.pop('expenses_list')
        property_related_serializer = PropertyRelatedSerializer(data=property_related)
        if property_related_serializer.is_valid():
            property_related_serializer.save()
            property_related_pk = property_related_serializer.data['property_related_id']
            PropertyRelated.objects.filter(property_related_id=property_related_pk).update(year_form=year_form_pk)
            for i in range(len(expenses_list)):
                expenses_list_serializer = ExpensesListSerializer(data=expenses_list[i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            name = "property_related"
            errors = property_related_serializer.errors
            return Response({"Serializer": name, "error": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Production Related
        for i in range(len(production_related)):
            production_expense_list = production_related[i].pop('expenses_list')
            production_related_serializer = ProductionRelatedSerializer(data=production_related[i])
            if production_related_serializer.is_valid():
                production_related_serializer.save()
                production_related_pk = production_related_serializer.data['production_related_id']
                ProductionRelated.objects.filter(production_related_id=production_related_pk).update(year_form=year_form_pk)
                for j in range(len(production_expense_list)):
                    production_related_expense_serializer = ProductionRelatedExpenseSerializer(data=production_expense_list[j])
                    if production_related_expense_serializer.is_valid():
                        production_related_expense_serializer.save()
                        production_related_expense_pk = production_related_expense_serializer.data['production_related_expense_id']
                        ProductionRelatedExpense.objects.filter(production_related_expense_id=production_related_expense_pk).update(production_related=production_related_pk)
                    else:
                        return Response(production_related_expense_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                name = "production_related"
                errors = production_related_serializer.errors
                return Response({"Serializer": name, "error": errors}, status=status.HTTP_400_BAD_REQUEST)    


        # Pay Roll Taxes And Benefits
        pay_roll_list = pay_roll_taxes_and_benefits.pop('pay_roll_list')
        pay_roll_taxes_and_benefits_serializer = PayRollTaxesAndBenefitsSerializer(data=pay_roll_taxes_and_benefits)
        if pay_roll_taxes_and_benefits_serializer.is_valid():
            pay_roll_taxes_and_benefits_serializer.save()
            pay_roll_taxes_and_benefits_pk = pay_roll_taxes_and_benefits_serializer.data['pay_roll_tax_and_benefits_id']
            PayRollTaxesAndBenefits.objects.filter(pay_roll_tax_and_benefits_id=pay_roll_taxes_and_benefits_pk).update(year_form=year_form_pk)
            for i in range(len(pay_roll_list)):
                pay_roll_list_serializer = PayRollListSerializer(data=pay_roll_list[i])
                if pay_roll_list_serializer.is_valid():
                    pay_roll_list_serializer.save()
                    pay_roll_list_pk = pay_roll_list_serializer.data['pay_roll_list_id']
                    PayRollList.objects.filter(pay_roll_list_id=pay_roll_list_pk).update(pay_roll_taxes_and_benefits=pay_roll_taxes_and_benefits_pk)
                else:
                    return Response(pay_roll_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(pay_roll_taxes_and_benefits_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Part Time Workers
        workers_list = part_time_workers.pop('workers_list')
        part_time_workers_serializer = PartTimeWorkersSerializer(data=part_time_workers)
        if part_time_workers_serializer.is_valid():
            part_time_workers_serializer.save()
            part_time_workers_pk = part_time_workers_serializer.data['part_time_workers_id']
            PartTimeWorkers.objects.filter(part_time_workers_id=part_time_workers_pk).update(year_form=year_form_pk)
            for i in range(len(workers_list)):
                workers_list_serializer = WorkersListSerializer(data=workers_list[i])
                if workers_list_serializer.is_valid():
                    workers_list_serializer.save()
                    workers_list_pk = workers_list_serializer.data['workers_list_id']
                    WorkersList.objects.filter(workers_list_id=workers_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(workers_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(part_time_workers_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Other Expenses
        expenses_list = other_expenses.pop('expenses_list')
        other_expenses_serializer = OtherExpensesSerializer(data=other_expenses)
        if other_expenses_serializer.is_valid():
            other_expenses_serializer.save()
            other_expenses_pk = other_expenses_serializer.data['other_expenses_id']
            OtherExpenses.objects.filter(other_expenses_id=other_expenses_pk).update(year_form=year_form_pk)
            for i in range(len(expenses_list)):
                expenses_list_serializer = ExpensesListSerializer(data=expenses_list[i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(other_expenses_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Office General Business
        expenses_list = office_general_business.pop('expenses_list')
        office_general_business_serializer = OfficeGeneralBusinessSerializer(data=office_general_business)
        if office_general_business_serializer.is_valid():
            office_general_business_serializer.save()
            office_general_business_pk = office_general_business_serializer.data['office_general_business_id']
            OfficeGeneralBusiness.objects.filter(office_general_business_id=office_general_business_pk).update(year_form=year_form_pk)
            for i in range(len(expenses_list)):
                expenses_list_serializer = ExpensesListSerializer(data=expenses_list[i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(office_general_business_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Marketing Expenses
        expenses_list = marketing_expenses.pop('expenses_list')
        marketing_expenses_serializer = MarketingExpensesSerializer(data=marketing_expenses)
        if marketing_expenses_serializer.is_valid():
            marketing_expenses_serializer.save()
            marketing_expenses_pk = marketing_expenses_serializer.data['marketing_expenses_id']
            MarketingExpenses.objects.filter(marketing_expenses_id=marketing_expenses_pk).update(year_form=year_form_pk)
            for i in range(len(expenses_list)):
                expenses_list_serializer = ExpensesListSerializer(data=expenses_list[i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(marketing_expenses_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Legal And Professional Services
        expenses_list = legal_and_professional_services.pop('expenses_list')
        legal_and_professional_services_serializer = LegalAndProfessionalServicesSerializer(data=legal_and_professional_services)
        if legal_and_professional_services_serializer.is_valid():
            legal_and_professional_services_serializer.save()
            legal_and_professional_services_pk = legal_and_professional_services_serializer.data['legal_and_professional_services_id']
            LegalAndProfessionalServices.objects.filter(legal_and_professional_services_id=legal_and_professional_services_pk).update(year_form=year_form_pk)
            for i in range(len(expenses_list)):
                expenses_list_serializer = ExpensesListSerializer(data=expenses_list[i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(legal_and_professional_services_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Funding Investment
        funding_investment_serializer = FundingInvestmentSerializer(data=funding_investment)
        if funding_investment_serializer.is_valid():
            funding_investment_serializer.save()
            funding_investment_pk = funding_investment_serializer.data['funding_investment_id']
            FundingInvestment.objects.filter(funding_investment_id=funding_investment_pk).update(year_form=year_form_pk)
        else:
            return Response(funding_investment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Full Time Workers
        workers_list = full_time_workers.pop('workers_list')
        full_time_workers_serializer = FullTimeWorkersSerializer(data=full_time_workers)
        if full_time_workers_serializer.is_valid():
            full_time_workers_serializer.save()
            full_time_workers_pk = full_time_workers_serializer.data['full_time_workers_id']
            FullTimeWorkers.objects.filter(full_time_workers_id=full_time_workers_pk).update(year_form=year_form_pk)
            for i in range(len(workers_list)):
                workers_list_serializer = WorkersListSerializer(data=workers_list[i])
                if workers_list_serializer.is_valid():
                    workers_list_serializer.save()
                    workers_list_pk = workers_list_serializer.data['workers_list_id']
                    WorkersList.objects.filter(workers_list_id=workers_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(workers_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(full_time_workers_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Founders Draw
        fd_pay_array = founders_draw.pop('founders_draw_pay_array')
        founders_draw_serializer = FoundersDrawSerializer(data=founders_draw)
        if founders_draw_serializer.is_valid():
            founders_draw_serializer.save()
            founders_draw_pk = founders_draw_serializer.data['founders_draw_id']
            FoundersDraw.objects.filter(founders_draw_id=founders_draw_pk).update(year_form=year_form_pk)
            for i in range(len(fd_pay_array)):
                founders_draw_pay_serializer = FoundersDrawPaySerializer(data={'pay_array': fd_pay_array[i]})
                if founders_draw_pay_serializer.is_valid():
                    founders_draw_pay_serializer.save()
                    founders_draw_pay_pk = founders_draw_pay_serializer.data['founders_draw_pay_id']
                    FoundersDrawPay.objects.filter(founders_draw_pay_id=founders_draw_pay_pk).update(founders_draw=founders_draw_pk)
                else:
                    return Response(founders_draw_pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(founders_draw_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Fixed Assets
        fixed_assets_serializer = FixedAssetsSerializer(data=fixed_assets)
        if fixed_assets_serializer.is_valid():
            fixed_assets_serializer.save()
            fixed_assets_pk = fixed_assets_serializer.data['fixed_assets_id']
            FixedAssets.objects.filter(fixed_assets_id=fixed_assets_pk).update(year_form=year_form_pk)
        else:
            return Response(fixed_assets_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Distributions
        distributions_serializer = DistributionsSerializer(data=distributions)
        if distributions_serializer.is_valid():
            distributions_serializer.save()
            distributions_pk = distributions_serializer.data['distributions_id']
            Distributions.objects.filter(distributions_id=distributions_pk).update(year_form=year_form_pk)
        else:
            return Response(distributions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Customer Segments
        for i in range(len(customer_segments)):
            monthly_data = customer_segments[i].pop('monthly_data')
            customer_segments_serializer = CustomerSegmentsSerializer(data=customer_segments[i])
            if customer_segments_serializer.is_valid():
                customer_segments_serializer.save()
                customer_segments_pk = customer_segments_serializer.data['customer_segment_id']
                CustomerSegments.objects.filter(customer_segment_id=customer_segments_pk).update(year_form=year_form_pk)

                for j in range(len(monthly_data)):
                    monthly_data_serializer = MonthlyDataSerializer(data=monthly_data[j])
                    if monthly_data_serializer.is_valid():
                        monthly_data_serializer.save()
                        monthly_data_pk = monthly_data_serializer.data['monthly_data_id']
                        MonthlyData.objects.filter(monthly_data_id=monthly_data_pk).update(customer_segment=customer_segments_pk)
                    else:
                        return Response(monthly_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Cash On Hand
        cash_on_hand_serializer = CashOnHandSerializer(data=cash_on_hand)
        if cash_on_hand_serializer.is_valid():
            cash_on_hand_serializer.save()
            cash_on_hand_pk = cash_on_hand_serializer.data['cash_on_hand_id']
            CashOnHand.objects.filter(cash_on_hand_id=cash_on_hand_pk).update(year_form=year_form_pk)
        else:
            return Response(cash_on_hand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Banking Fees
        banking_fees_serializer = BankingFeesSerializer(data={"total_monthly": banking_fees['total_monthly']})
        if banking_fees_serializer.is_valid():
            banking_fees_serializer.save()
            banking_fees_pk = banking_fees_serializer.data['banking_fees_id']
            BankingFees.objects.filter(banking_fees_id=banking_fees_pk).update(year_form=year_form_pk)
            for i in range(len(banking_fees['expenses_list'])):
                expenses_list_serializer = ExpensesListSerializer(data=banking_fees['expenses_list'][i])
                if expenses_list_serializer.is_valid():
                    expenses_list_serializer.save()
                    expenses_list_pk = expenses_list_serializer.data['expenses_list_id']
                    ExpensesList.objects.filter(expenses_list_id=expenses_list_pk).update(year_form=year_form_pk)
                else:
                    return Response(expenses_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(banking_fees_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Additional Revenue
        additional_revenue_serializer = AdditionalRevenueSerializer(data=additional_revenue)
        if additional_revenue_serializer.is_valid():
            additional_revenue_serializer.save()
            additional_revenue_pk = additional_revenue_serializer.data['additional_revenue_id']
            AdditionalRevenue.objects.filter(additional_revenue_id=additional_revenue_pk).update(year_form=year_form_pk)
        else:
            return Response(additional_revenue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Status": "HTTP 201: Created"}, status=status.HTTP_201_CREATED)


class TestRowFlattenEndpoint(APIView):
    # THIS ENDPOINT IS FOR TEST PURPOSES ONLY!!

    def post(self, request):
        customer_segments_year3 = request.data.get('customerSegmentsYear3')
        customer_segments_year2 = request.data.get('customerSegmentsYear2')
        customer_segments_year1 = request.data.get('customerSegmentsYear1')

        data_dict_year1 = flatten_revform_rows_json(customer_segments_year3, 'customerSegmentsYear3')

        return Response(data_dict_year1, status=status.HTTP_202_ACCEPTED)
    
