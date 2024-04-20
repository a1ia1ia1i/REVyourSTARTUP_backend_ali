from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


# Serializer for Django Built-in User class
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MainFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainForm
        fields = '__all__'


class RevFormSerializer(serializers.ModelSerializer):    
    class Meta:
        model = RevForm
        fields = '__all__'


class RevFormRowsIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevFormRowsIndex
        fields = '__all__'


class RevFormRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevFormRows
        fields = '__all__'


class ProFormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProForma
        fields = '__all__'


class ProFormaFoundersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProFormaFounders
        fields = '__all__'


class DepreciationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepreciationForm
        fields = '__all__'


class DepreciationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepreciationSchedule
        fields = '__all__'


class YearFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearForm
        fields = '__all__'


class ExpensesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesList
        fields = '__all__'


class AdditionalRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalRevenue
        fields = '__all__'


class BankingFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankingFees
        fields = '__all__'


class CashOnHandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashOnHand
        fields = '__all__'


class CustomerSegmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSegments
        fields = '__all__'


class MonthlyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyData
        fields = '__all__'


class DistributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributions
        fields = '__all__'


class FixedAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAssets
        fields = '__all__'


class FoundersDrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundersDraw
        fields = '__all__'


class FoundersDrawPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundersDrawPay
        fields = '__all__'


class WorkersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkersList
        fields = '__all__'

class FullTimeWorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullTimeWorkers
        fields = '__all__'


class PartTimeWorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTimeWorkers
        fields = '__all__'


class SalariedWorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalariedWorkers
        fields = '__all__'


class FundingInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingInvestment
        fields = '__all__'


class LegalAndProfessionalServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalAndProfessionalServices
        fields = '__all__'


class MarketingExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingExpenses
        fields = '__all__'


class OfficeGeneralBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeGeneralBusiness
        fields = '__all__'


class OtherExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherExpenses
        fields = '__all__'


class PayRollTaxesAndBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRollTaxesAndBenefits
        fields = '__all__'


class PayRollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRollList
        fields = '__all__'


class ProductionRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRelated
        fields = '__all__'


class ProductionRelatedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRelatedExpense
        fields = '__all__'


class PropertyRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyRelated
        fields = '__all__'


class TravelVehicleRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelVehicleRelated
        fields = '__all__'


class WorkersHeadCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkersHeadCount
        fields = '__all__'

