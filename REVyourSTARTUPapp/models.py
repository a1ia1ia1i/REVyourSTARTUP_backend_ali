from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

#TODO: create appropriate models for rev form applicable to the json interface

class MainForm(models.Model):
    # This model will work as the 'Hub' for attaching all the different forms onto
    # by a specific user's id as a primary key. All of the seperate forms will be a foriegn key
    
    main_form_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    form_name = models.CharField(blank=True, null=True, max_length=255)
    rev_form = models.ForeignKey('RevForm', on_delete=models.CASCADE, blank=True, null=True)
    pro_forma = models.ForeignKey('ProForma', on_delete=models.CASCADE, blank=True, null=True)
    depreciation_form = models.ForeignKey('DepreciationForm', on_delete=models.CASCADE, blank=True, null=True)
    year1_form = models.ForeignKey("YearForm", on_delete=models.CASCADE, blank=True, null=True, related_name='year1')
    year2_form = models.ForeignKey("YearForm", on_delete=models.CASCADE, blank=True, null=True, related_name='year2')
    year3_form = models.ForeignKey("YearForm", on_delete=models.CASCADE, blank=True, null=True, related_name='year3')

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.form_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MainForm, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'main_form'


class RevForm(models.Model):
    # The main table for the revform
    
    # Refer to dataStructure_RevForm.json for visualization of table columns
    rev_form_id = models.AutoField(primary_key=True)

    # "valuationParameters"
    last_year_total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    amount_needed = models.DecimalField(max_digits=12, decimal_places=2)
    
    # "hit3YearGoals"
    three_years_effective_interest = models.DecimalField(max_digits=12, decimal_places=2)
    five_years_effective_interest = models.DecimalField(max_digits=12, decimal_places=2)
    seven_years_effective_interest = models.DecimalField(max_digits=12, decimal_places=2)
    
    revenue_multiplier = models.IntegerField()
    exit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # "exitYears"
    year0_percentage = models.IntegerField()
    year0_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year0_force_to = models.IntegerField()
    year1_percentage = models.IntegerField()
    year1_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year1_force_to = models.IntegerField()
    year2_percentage = models.IntegerField()
    year2_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year2_force_to = models.IntegerField()
    year3_percentage = models.IntegerField()
    year3_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year3_force_to = models.IntegerField()
    year4_percentage = models.IntegerField()
    year4_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year4_force_to = models.IntegerField()
    year5_percentage = models.IntegerField()
    year5_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year5_force_to = models.IntegerField()

    equity_percentage = models.IntegerField()
    year3_company_worth = models.DecimalField(max_digits=12, decimal_places=2)
    exit_revenue_multiplier = models.IntegerField()
    revenue_needed_year3 = models.DecimalField(max_digits=12, decimal_places=2)
    growth_projection = models.IntegerField()
    # end "valuationParameters"

    # "realityCheck1"
    total_market = models.DecimalField(max_digits=12, decimal_places=2)
    captured_at_year5 = models.DecimalField(max_digits=12, decimal_places=2)


    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(RevForm, self).save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'rev_form'


class RevFormRowsIndex(models.Model):
    # This table acts as an index for referring to the different customer segments, the field
    # 'revform_rows_name' should be named accordingly. This will provide a single point of indexing
    # all of the different row entries, which are not known at the time of revform creation.

    revform_rows_index_id = models.AutoField(primary_key=True)
    rev_form= models.ForeignKey(RevForm, on_delete=models.CASCADE, blank=True, null=True, related_name='rev_form')

    # This name can correlate to "customerSegmentsYear3" or "customerSegmentsYear1" etc...
    revform_rows_name = models.CharField(max_length=255)

    row_count = models.IntegerField()

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.revform_rows_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(RevFormRowsIndex, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'rev_form_rows_index'


class RevFormRows(models.Model):
    # This table is referred to by the index, and will carry the information of applicable to
    # individual rows in the revform

    revform_rows_id = models.AutoField(primary_key=True)
    revform_rows_index = models.ForeignKey(RevFormRowsIndex, on_delete=models.CASCADE, blank=True, null=True)

    segment_name = models.CharField(max_length=255)
    avg_revenue_per_customer = models.DecimalField(max_digits=12, decimal_places=2)
    quick_modeling_percentage = models.IntegerField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    customers = models.IntegerField()
    your_percentage = models.DecimalField(max_digits=12, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.segment_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(RevFormRows, self).save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'revform_rows'


class ProForma(models.Model):
    # Main table for Pro Forma
    pro_forma_id = models.AutoField(primary_key=True)
    
    # calendar
    start_year = models.IntegerField()
    start_month = models.IntegerField()
    
    start_capital = models.IntegerField()
    
    # foundersDraw
    number_of_founders = models.IntegerField()
    # founders list goes here

    # profitFirst
    #percentageOfIncomeDistributed
    year1_pid = models.IntegerField()
    year2_pid = models.IntegerField()
    year3_pid = models.IntegerField()
    year4_pid = models.IntegerField()
    year5_pid = models.IntegerField()

    include_investments = models.CharField(max_length=3)

    # incomeAndExpenses
    # years
    year1_income = models.DecimalField(max_digits=12, decimal_places=2)
    year1_distribution = models.DecimalField(max_digits=12, decimal_places=2)
    year1_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    year1_margin = models.DecimalField(max_digits=12, decimal_places=2)
    year2_income = models.DecimalField(max_digits=12, decimal_places=2)
    year2_distribution = models.DecimalField(max_digits=12, decimal_places=2)
    year2_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    year2_margin = models.DecimalField(max_digits=12, decimal_places=2)
    year3_income = models.DecimalField(max_digits=12, decimal_places=2)
    year3_distribution = models.DecimalField(max_digits=12, decimal_places=2)
    year3_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    year3_margin = models.DecimalField(max_digits=12, decimal_places=2)
    year4_income = models.DecimalField(max_digits=12, decimal_places=2)
    year4_distribution = models.DecimalField(max_digits=12, decimal_places=2)
    year4_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    year4_margin = models.DecimalField(max_digits=12, decimal_places=2)
    year5_income = models.DecimalField(max_digits=12, decimal_places=2)
    year5_distribution = models.DecimalField(max_digits=12, decimal_places=2)
    year5_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    year5_margin = models.DecimalField(max_digits=12, decimal_places=2)

    # cashFlow
    exclude_depreciation = models.CharField(max_length=3)

    # minimumCashOnHandPerYear
    year1_first_negative_month = models.DecimalField(max_digits=12, decimal_places=2)
    year1_first_negative_month_amount = models.DecimalField(max_digits=12, decimal_places=2)
    year1_minimum_this_year = models.DecimalField(max_digits=12, decimal_places=2)
    year2_first_negative_month = models.DecimalField(max_digits=12, decimal_places=2)
    year2_first_negative_month_amount = models.DecimalField(max_digits=12, decimal_places=2)
    year2_minimum_this_year = models.DecimalField(max_digits=12, decimal_places=2)
    year3_first_negative_month = models.DecimalField(max_digits=12, decimal_places=2)
    year3_first_negative_month_amount = models.DecimalField(max_digits=12, decimal_places=2)
    year3_minimum_this_year = models.DecimalField(max_digits=12, decimal_places=2)

    # maxHeadCountPerYear
    year1_founders = models.IntegerField()
    year1_salaries = models.IntegerField()
    year1_fulltime = models.IntegerField()
    year1_parttime = models.IntegerField()
    year2_founders = models.IntegerField()
    year2_salaries = models.IntegerField()
    year2_fulltime = models.IntegerField()
    year2_parttime = models.IntegerField()
    year3_founders = models.IntegerField()
    year3_salaries = models.IntegerField()
    year3_fulltime = models.IntegerField()
    year3_parttime = models.IntegerField()
    year4_founders = models.IntegerField()
    year4_salaries = models.IntegerField()
    year4_fulltime = models.IntegerField()
    year4_parttime = models.IntegerField()
    year5_founders = models.IntegerField()
    year5_salaries = models.IntegerField()
    year5_fulltime = models.IntegerField()
    year5_parttime = models.IntegerField()


    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ProForma, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "pro_forma"


class ProFormaFounders(models.Model):
    pro_forma_founder_id = models.AutoField(primary_key=True)
    pro_forma = models.ForeignKey(ProForma, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    compensation_at_year3 = models.IntegerField()
    year1_percent = models.IntegerField()
    year1_total = models.DecimalField(max_digits=12, decimal_places=2)
    year2_percent = models.IntegerField()
    year2_total = models.DecimalField(max_digits=12, decimal_places=2)
    year3_percent = models.IntegerField()
    year3_total = models.DecimalField(max_digits=12, decimal_places=2)
    year4_percent = models.IntegerField()
    year4_total = models.DecimalField(max_digits=12, decimal_places=2)
    year5_percent = models.IntegerField()
    year5_total = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ProFormaFounders, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "pro_forma_founders"


class DepreciationForm(models.Model):
    depreciation_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_month = models.IntegerField()
    start_year = models.IntegerField()
    value_at_time = models.IntegerField()
    years_left = models.IntegerField()
    salvage_value = models.IntegerField()
    method = models.CharField(max_length=255)
    off_sheet = models.IntegerField()


    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(DepreciationForm, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "depreciation_form"


class DepreciationSchedule(models.Model):
    depreciation_schedule_id = models.AutoField(primary_key=True)
    depreciation_form = models.ForeignKey(DepreciationForm, on_delete=models.CASCADE, blank=True, null=True)
    date = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(DepreciationSchedule, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "depreciation_schedule"

# MODELS FOR YEAR FORMS START HERE
class YearForm(models.Model):
    year_form_id = models.AutoField(primary_key=True)
    
    # To distinguish between year1, year2, and year3
    which_year = models.IntegerField()

    # additionalRevenue (done)
    # bankingFees (done)
    # cashOnHand (done)
    # customerSegments (done)
    # distributions (done)
    # fixedAssets (done)
    # foundersDraw (done)
    # fullTimeWorkers (done)
    # fundingInvestment (done)
    # legalAndProfessionalServices (done)
    # marketingExpenses (done)
    # officeGeneralBusiness (done)
    # otherExpenses (done)
    # partTimeWorkers (done)
    # payRollTaxesAndBenefits (done)
    # productionRelated (done)
    # propertyRelated (done)
    # returnReworks (done)
    # salariedWorkers (done)
    # travelVehicleRelated (done)
    # workersHeadCount (done)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(YearForm, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "year_form"


class AdditionalRevenue(models.Model):
    additional_revenue_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # Condense String Lists
    source_names = models.CharField(max_length=511)
    sources = models.CharField(max_length=511)

    # Will be floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(AdditionalRevenue, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "additional_revenue"


class BankingFees(models.Model):
    banking_fees_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # Will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(BankingFees, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "banking_fees"


class CashOnHand(models.Model):
    cash_on_hand_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    exclude_depreciation = models.BooleanField()
    initial_cash_on_hand = models.DecimalField(max_digits=12, decimal_places=2)

    # These will both hold floats
    with_depreciation = models.CharField(max_length=511)
    without_depreciation = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(CashOnHand, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "cash_on_hand"


class CustomerSegments(models.Model):
    customer_segment_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # inputData
    commission = models.DecimalField(max_digits=12, decimal_places=2)
    delivered_in = models.IntegerField()
    deposit = models.DecimalField(max_digits=12, decimal_places=2)
    extra_months = models.IntegerField()
    fixed_fees = models.DecimalField(max_digits=12, decimal_places=2)

    # monthlyData has its own table

    name = models.CharField(max_length=255)
    number_to_sell = models.IntegerField()
    numbers_to_sell_original = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=255)

    # this will contain floats
    total_monthly_data = models.CharField(max_length=2047)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(CustomerSegments, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "customer_segments"


class MonthlyData(models.Model):
    # This table is part of customerSegments

    monthly_data_id = models.AutoField(primary_key=True)
    customer_segment = models.ForeignKey(CustomerSegments, on_delete=models.CASCADE, blank=True, null=True)

    numbers_sold = models.IntegerField()
    deposit = models.DecimalField(max_digits=12, decimal_places=2)
    original = models.DecimalField(max_digits=12, decimal_places=2)
    extra_from_previous_months = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MonthlyData, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "monthly_data"


class Distributions(models.Model):
    distributions_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    include_investments = models.BooleanField()
    percent_of_income_distributed = models.DecimalField(max_digits=12, decimal_places=2)

    # These will contain floats
    with_investments = models.CharField(max_length=511)
    without_investments = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(Distributions, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "distributions"


class FixedAssets(models.Model):
    fixed_assets_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # These will all contain floats
    new_acquisitions = models.CharField(max_length=511)
    depreciation = models.CharField(max_length=511)
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(FixedAssets, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "fixed_assets"


class FoundersDraw(models.Model):
    founders_draw_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    number_of_founders = models.IntegerField()
    founders_share = models.DecimalField(max_digits=12, decimal_places=2)

    # This will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(FoundersDraw, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "founders_draw"


class FoundersDrawPay(models.Model):
    # This is connected to FoundersDraw
    founders_draw_pay_id = models.AutoField(primary_key=True)
    founders_draw = models.ForeignKey(FoundersDraw, on_delete=models.CASCADE, blank=True, null=True)

    # This will contain floats
    pay_array = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(FoundersDrawPay, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "founders_draw_pay"


class FullTimeWorkers(models.Model):
    full_time_workers_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # This will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(FullTimeWorkers, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "full_time_workers"


class PartTimeWorkers(models.Model):
    part_time_workers_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # This will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(PartTimeWorkers, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "part_time_workers"


class SalariedWorkers(models.Model):
    salaried_workers_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # This will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(SalariedWorkers, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "salaried_workers"


class WorkersList(models.Model):
    # This is connected to FullTimeWorkers or PartTimeWorkers or SalariedWorkers
    workers_list_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # This will be differentiated by tags associated with "workersList"
    # The only valid possible tag_name's are
    #(full_time_workers, part_time_workers, salaried_workers)
    tag_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2)

    # This will contain floats
    monthly_data = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(WorkersList, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "workers_list"


class FundingInvestment(models.Model):
    funding_investment_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # These are variable length
    
    # This will require using the string parsing functions in yearformparse.py
    source_names = models.CharField(max_length=1023)
    
    # These will contain floats
    sources = models.CharField(max_length=511)
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(FundingInvestment, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "funding_investment"


class LegalAndProfessionalServices(models.Model):
    legal_and_professional_services_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # This will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(LegalAndProfessionalServices, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "legal_and_professional_services"
    

class MarketingExpenses(models.Model):
    marketing_expenses_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MarketingExpenses, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "marketing_expenses"


class OfficeGeneralBusiness(models.Model):
    office_general_business_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(OfficeGeneralBusiness, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "office_general_business"


class OtherExpenses(models.Model):
    other_expenses_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(OtherExpenses, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "other_expenses"


class PropertyRelated(models.Model):
    property_related_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(PropertyRelated, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "property_related"


class TravelVehicleRelated(models.Model):
    travel_vehicle_related_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(TravelVehicleRelated, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "travel_vehicle_related"


class ExpensesList(models.Model):
    # This table will act as a general table for all the "expensesList" tags in the year forms
    # This is most easily done by naming the expenses list as the same tag it is associated with in
    # the json. The list of possible names that name can take is:
    # (banking_fees, legal_and_professional_services, marketing_expenses, office_general_business, 
    #  other_expenses, property_related, return_reworks, travel_vehicle_related)

    # "returnReworks" DOES NOT HAVE AN ASSOCIATED totalMonthly THEREFORE IT CAN JUST BE USED AS A 
    # tag_name AND ACCESSED THAT WAY

    expenses_list_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # Corresponds to the tagname in the json
    tag_name = models.CharField(max_length=255)

    source_name = models.CharField(max_length=255)
    
    # This will contain floats
    monthly_data = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExpensesList, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "expenses_list"


class PayRollTaxesAndBenefits(models.Model):
    pay_roll_tax_and_benefits_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # This will hold floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(PayRollTaxesAndBenefits, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "pay_roll_taxes_and_benefits"


class PayRollList(models.Model):
    pay_roll_list_id = models.AutoField(primary_key=True)
    pay_roll_taxes_and_benefits = models.ForeignKey(PayRollTaxesAndBenefits, on_delete=models.CASCADE, blank=True, null=True)

    source_name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    
    # This will hold floats
    monthly_data = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(PayRollList, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "pay_roll_list"



class ProductionRelated(models.Model):
    production_related_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)

    # This will contain floats
    total_monthly = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ProductionRelated, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "production_related"


class ProductionRelatedExpense(models.Model):
    production_related_expense_id = models.AutoField(primary_key=True)
    production_related = models.ForeignKey(ProductionRelated, on_delete=models.CASCADE, blank=True, null=True)

    source_name = models.CharField(max_length=255)
    
    # This will contain floats
    monthly_data = models.CharField(max_length=511)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ProductionRelatedExpense, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "production_related_expense"


class WorkersHeadCount(models.Model):
    workers_head_count_id = models.AutoField(primary_key=True)
    year_form = models.ForeignKey(YearForm, on_delete=models.CASCADE, blank=True, null=True)

    # These will all contain integers
    founders_head_count = models.CharField(max_length=255)
    salaried_head_count = models.CharField(max_length=255)
    full_time_head_count = models.CharField(max_length=255)
    part_time_head_count = models.CharField(max_length=255)
    total_monthly = models.CharField(max_length=255)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(WorkersHeadCount, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = "workers_head_count"

