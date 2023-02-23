from django.db import models
# from .fields import AddressField, ForeignKeyField, MoneyField, CharField, DateTimeField, BooleanField, ManyToManyField
from .signals import pre_save, post_save
from .fields import (PrimaryKeyField, EmailField, CharField,
                     BooleanField, DateTimeField, DateField,
                     ManyToManyField, ForeignKeyField,
                     MoneyField, IntegerField, DisputeReasonField, RelatedManager, DictField, AddressField,
                     DebitedBankAccountField,
                     ShippingAddressField, RefundReasonField, ListField, ReportTransactionsFiltersField,
                     ReportWalletsFiltersField, BillingField, SecurityInfoField, PlatformCategorizationField,
                     BirthplaceField, ApplepayPaymentDataField, GooglepayPaymentDataField, ScopeBlockedField,
                     BrowserInfoField, ShippingField, CurrentStateField, FallbackReasonField, InstantPayoutField,
                     CountryAuthorizationDataField, PayinsLinkedField)
from .base import BaseApiModel
from . import constants
from .query import InsertQuery, UpdateQuery, SelectQuery, ActionQuery
from .utils import Money, Address, Birthplace
import time

class BaseModel(BaseApiModel):
    # id = PrimaryKeyField(api_name='Id')
    tag = models.CharField() # api_name='Tag'
    update_date = models.DateTimeField() #api_name='UpdateDate'

class User(BaseModel):
    email = models.EmailField(null=False) # api_name='Email'
    kyc_level = models.CharField(choices=constants.KYC_LEVEL, default=constants.KYC_LEVEL.light) # api_name='KYCLevel'
    terms_and_conditions_accepted = models.BooleanField() # api_name='TermsAndConditionsAccepted'
    terms_and_conditions_accepted_date = models.DateTimeField() # api_name='TermsAndConditionsAcceptedDate'
    user_category = models.CharField() # api_name='UserCategory'

    def fixed_kwargs(self):
        return {"user_id": self.id}

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # self.disputes = RelatedManager(self, Dispute)

    @classmethod
    def cast(cls, result):
        if 'PersonType' in result:
            if result['PersonType'] == 'NATURAL':
                # return NaturalUser
                return "NaturalUser"
            elif result['PersonType'] == 'LEGAL':
                # return LegalUser
                return "LegalUser"

        return cls

    def get_emoney(self, *args, **kwargs):
        kwargs['user_id'] = self.id
        select = SelectQuery(EMoney, *args, **kwargs)
        if kwargs.__contains__('month') and kwargs.__contains__('year'):
            select.identifier = 'FOR_MONTH'
        elif kwargs.__contains__('year'):
            select.identifier = 'FOR_YEAR'
        else:
            select.identifier = 'ALL'
        return select.all(*args, **kwargs)

    def get_pre_authorizations(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(PreAuthorization, *args, **kwargs)
        select.identifier = 'USER_GET_PREAUTHORIZATIONS'
        return select.all(*args, **kwargs)

    def get_block_status(self, *args, **kwargs):
        kwargs['user_id'] = self.id
        select = SelectQuery(UserBlockStatus, *args, **kwargs)
        select.identifier = 'USERS_BLOCK_STATUS'
        return select.get("", *args, **kwargs)

    def get_regulatory(self, *args, **kwargs):
        kwargs['user_id'] = self.id
        select = SelectQuery(UserBlockStatus, *args, **kwargs)
        select.identifier = 'USERS_REGULATORY'
        return select.get("", *args, **kwargs)

    def __str__(self):
        return '%s' % self.email

class BankAccount(models.Model):
    # Quitar default, son solo para ejemplo
    user = ForeignKeyField(User, api_name='UserId', related_name='bankaccounts')
    type = models.CharField(null=False, default="IBAN", max_length=100)
    owner_address = AddressField(null=False, default="")
    owner_name = models.CharField(null=False, default="Joe", max_length=100)
    tag = models.CharField(null=False, default="custom meta", max_length=100)
    created_at = models.IntegerField(default=int(time.time()))
    active = models.BooleanField(default=True) # api_name='Active'
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = int(time.time())
        return super().save(*args, **kwargs)

class EMoney(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', related_name='emoney')
    credited_emoney = MoneyField(api_name='CreditedEMoney')
    debited_emoney = MoneyField(api_name='DebitedEMoney')

    class Meta:
        verbose_name = 'emoney'
        url = {
            'ALL': '/users/%(user_id)s/emoney',
            'FOR_YEAR': '/users/%(user_id)s/emoney/%(year)s',
            'FOR_MONTH': '/users/%(user_id)s/emoney/%(year)s/%(month)s'
        }

    def __str__(self):
        return 'EMoney for user %s' % self.user_id

class Card(BaseModel):
    creation_date = DateTimeField(api_name='CreationDate')
    expiration_date = CharField(api_name='ExpirationDate')
    alias = CharField(api_name='Alias')
    card_provider = CharField(api_name='CardProvider')
    card_type = CharField(api_name='CardType',
                          choices=constants.CARD_TYPE_CHOICES,
                          default=None)
    country = CharField(api_name='Country')
    product = CharField(api_name='Product')
    bank_code = CharField(api_name='BankCode')
    active = BooleanField(api_name='Active')
    currency = CharField(api_name='Currency')
    validity = CharField(api_name='Validity',
                         choices=constants.VALIDITY_CHOICES,
                         default=constants.VALIDITY_CHOICES.unknown)
    user = ForeignKeyField(User, api_name='UserId', required=True, related_name='cards')
    fingerprint = CharField(api_name='Fingerprint')

    @classmethod
    def get_by_fingerprint(cls, fingerprint, *args, **kwargs):
        kwargs['fingerprint'] = fingerprint
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'CARDS_FOR_FINGERPRINT'
        return select.all(*args, **kwargs)

    def get_pre_authorizations(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(PreAuthorization, *args, **kwargs)
        select.identifier = 'CARD_PRE_AUTHORIZATIONS'
        return select.all(*args, **kwargs)

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'CARD_GET_TRANSACTIONS'
        return select.all(*args, **kwargs)

    def validate(self, *args, **kwargs):
        kwargs['id'] = self.id
        insert = InsertQuery(self, **kwargs)
        insert.identifier = 'CARD_VALIDATE'
        return insert.execute()

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        url = {
            SelectQuery.identifier: '/cards',
            UpdateQuery.identifier: '/cards',
            'CARDS_FOR_FINGERPRINT': '/cards/fingerprints/%(fingerprint)s',
            'CARD_VALIDATE': '/cards/%(id)s/validate'}

    def __str__(self):
        return '%s of user %s' % (self.card_type, self.user_id)

class Wallet(BaseModel):
    owners = ManyToManyField(User, api_name='Owners', related_name='wallets', required=True)
    description = CharField(api_name='Description', required=True)
    currency = CharField(api_name='Currency', required=True)
    balance = MoneyField(api_name='Balance')
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'
        url = '/wallets'

    def __init__(self, *args, **kwargs):
        super(Wallet, self).__init__(*args, **kwargs)
        self.disputes = RelatedManager(self, Dispute)

    def __str__(self):
        return 'Wallet n.%s' % self.id

    @classmethod
    def is_client_wallet(cls, obj):
        if isinstance(obj, Wallet) or isinstance(obj, ClientWallet):
            test_id = obj.id
        elif isinstance(obj, str):
            test_id = obj
        else:
            return False
        if test_id.startswith('FEES_') or \
                test_id.startswith('DEFAULT_') or \
                test_id.startswith('CREDIT_'):
            return True
        return False

    @classmethod
    def get(cls, *args, **kwargs):
        if len(args) == 1 and cls.is_client_wallet(args[0]):
            return ClientWallet.get(*tuple(args[0].split('_')), **kwargs)
        return super(Wallet, cls).get(*args, **kwargs)


class PayIn(BaseModel):
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', related_name='credited_users')
    credited_funds = MoneyField(api_name='CreditedFunds')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType', choices=constants.PAYIN_PAYMENT_TYPE, default=None)
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)

    def get_refunds(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Refund, args, kwargs)
        select.identifier = 'PAYIN_GET_REFUNDS'
        return select.all(*args, **kwargs)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = '/payins'

    @classmethod
    def cast(cls, result):
        if cls.__name__ == "RecurringPayInCIT":
            return RecurringPayInCIT

        if cls.__name__ == "RecurringPayInMIT":
            return RecurringPayInMIT

        payment_type = result.get('PaymentType')
        execution_type = result.get('ExecutionType')

        types = {
            ("CARD", "DIRECT"): DirectPayIn,
            ("CARD", "WEB"): CardWebPayIn,
            ("DIRECT_DEBIT", "DIRECT"): DirectDebitDirectPayIn,
            ("DIRECT_DEBIT", "WEB"): DirectDebitWebPayIn,
            ("PREAUTHORIZED", "DIRECT"): PreAuthorizedPayIn,
            ("BANK_WIRE", "DIRECT"): BankWirePayIn,
            ("BANK_WIRE", "EXTERNAL_INSTRUCTION"): BankWirePayInExternalInstruction,
            ("APPLEPAY", "DIRECT"): ApplepayPayIn,
            ("GOOGLEPAY", "DIRECT"): GooglepayPayIn
        }

        return types.get((payment_type, execution_type), cls)


class PreAuthorization(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    remaining_funds = MoneyField(api_name='RemainingFunds')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    payment_status = CharField(api_name='PaymentStatus', choices=constants.PAYMENT_STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default,
                            required=True)
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    expiration_date = DateTimeField(api_name='ExpirationDate')
    payin = ForeignKeyField(PayIn, api_name='PayInId')
    billing = BillingField(api_name='Billing')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    multi_capture = BooleanField(api_name='MultiCapture')
    ip_address = CharField(api_name='IpAddress')
    browser_info = BrowserInfoField(api_name='BrowserInfo')
    shipping = ShippingField(api_name='Shipping')
    requested_3ds_version = CharField(api_name='Requested3DSVersion')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'PRE_AUTHORIZATION_TRANSACTIONS'
        return select.all(*args, **kwargs)

    class Meta:
        verbose_name = 'preauthorization'
        verbose_name_plural = 'preauthorizations'
        url = {
            InsertQuery.identifier: '/preauthorizations/card/direct',
            UpdateQuery.identifier: '/preauthorizations',
            SelectQuery.identifier: '/preauthorizations',
            'USER_GET_PREAUTHORIZATIONS': '/users/%(id)s/preauthorizations',
            'CARD_PRE_AUTHORIZATIONS': '/cards/%(id)s/preauthorizations'
        }

class UserBlockStatus(BaseModel):
    scope_blocked = ScopeBlockedField(api_name='ScopeBlocked', required=True)
    action_code = CharField(api_name='ActionCode', required=True)

    class Meta:
        verbose_name = 'userblockstatus'
        verbose_name_plural = 'userblockstatuses'

        url = {
            'USERS_BLOCK_STATUS': '/users/%(user_id)s/blockStatus',
            'USERS_REGULATORY': '/users/%(user_id)s/Regulatory'
        }

class Refund(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    refund_reason = RefundReasonField(api_name='RefundReason')
    initial_transaction_id = CharField(api_name='InitialTransactionId')
    initial_transaction_type = CharField(api_name='InitialTransactionType', choices=constants.TRANSACTION_TYPE_CHOICES,
                                         default=None)

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = {
            SelectQuery.identifier: '/refunds',
            InsertQuery.identifier: '/refunds',
            UpdateQuery.identifier: '/refunds',
            'REPUDIATION_GET_REFUNDS': '/repudiations/%(id)s/refunds',
            'TRANSFER_GET_REFUNDS': '/transfers/%(id)s/refunds',
            'PAYOUT_GET_REFUNDS': '/payouts/%(id)s/refunds',
            'PAYIN_GET_REFUNDS': '/payins/%(id)s/refunds'
        }

class Transaction(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', related_name='transactions')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')
    debited_funds = MoneyField(api_name='DebitedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    wallet = ForeignKeyField(Wallet, related_name='transactions')
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        url = {
            SelectQuery.identifier: '/users/%(user_id)s/transactions',
            InsertQuery.identifier: '/users/%(user_id)s/transactions',
            UpdateQuery.identifier: '/users/%(user_id)s/transactions',
            'MANDATE_GET_TRANSACTIONS': '/mandates/%(id)s/transactions',
            'CARD_GET_TRANSACTIONS': '/cards/%(id)s/transactions',
            'BANK_ACCOUNT_GET_TRANSACTIONS': '/bankaccounts/%(id)s/transactions',
            'PRE_AUTHORIZATION_TRANSACTIONS': '/preauthorizations/%(id)s/transactions'
        }

    def __str__(self):
        return 'Transaction n.%s' % self.id

class Dispute(BaseModel):
    initial_transaction_id = CharField(api_name='InitialTransactionId')
    initial_transaction_type = CharField(api_name='InitialTransactionType', choices=constants.TRANSACTION_TYPE_CHOICES,
                                         default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    dispute_reason = DisputeReasonField(api_name='DisputeReason')
    status = CharField(api_name='Status', choices=constants.DISPUTES_STATUS_CHOICES, default=None)
    status_message = CharField(api_name='StatusMessage')
    disputed_funds = MoneyField(api_name='DisputedFunds')
    contested_funds = MoneyField(api_name='ContestedFunds')
    repudiation_id = CharField(api_name='RepudiationId')

    dispute_type = CharField(api_name='DisputeType', choices=constants.DISPUTE_TYPE_CHOICE, default=None)
    contest_deadline_date = DateTimeField(api_name='ContestDeadlineDate')

    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'dispute'
        verbose_name_plural = 'disputes'
        url = {
            SelectQuery.identifier: '/disputes',
            UpdateQuery.identifier: '/disputes',
            'CLOSE_DISPUTE': '/disputes/%(id)s/close/',
            'SUBMIT_DISPUTE': '/disputes/%(id)s/submit/',
            'RE_SUBMIT_DISPUTE': '/disputes/%(id)s/submit/',
            'PENDING_SETTLEMENT': '/disputes/pending-settlement'
        }

    def __init__(self, *args, **kwargs):
        super(Dispute, self).__init__(*args, **kwargs)
        self.transactions = RelatedManager(self, Transaction)

    def __str__(self):
        return 'Dispute n.%s tag:%s' % (self.id, self.tag)

    def save(self, handler=None, cls=None):
        self._handler = handler or self.handler

        if cls is None:
            cls = self.__class__

        created = False

        pre_save.send(cls, instance=self)

        update = self.update(
            self.get_pk(),
            **{'tag': self.tag}
        )
        result = update.execute(handler)

        post_save.send(cls, instance=self, created=created)

        for key, value in result.items():
            setattr(self, key, value)

        return result

    def close(self, handler=None):
        self._handler = handler or self.handler
        action = ActionQuery(
            Dispute,
            self.get_pk(),
            'CLOSE_DISPUTE'
        )
        action.execute(handler)

    def contest(self, money, handler=None):
        self._handler = handler or self.handler
        if isinstance(money, Money):
            action = ActionQuery(
                Dispute,
                self.get_pk(),
                'SUBMIT_DISPUTE',
                **{'ContestedFunds': MoneyField().api_value(money)}
            )
            return action.execute(handler)

    def resubmit(self, handler=None):
        self._handler = handler or self.handler
        action = ActionQuery(
            Dispute,
            self.get_pk(),
            'RE_SUBMIT_DISPUTE'
        )
        return action.execute(handler)

    @classmethod
    def get_pending_settlement(cls, *args, **kwargs):
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'PENDING_SETTLEMENT'
        return select.all(*args, **kwargs)

class ClientWallet(Wallet):
    funds_type = CharField(api_name='FundsType')

    class Meta:
        verbose_name = 'client_wallets'
        verbose_name_plural = 'client_wallets'
        fund_type_url = {
            'CREDIT': 'SELECT_BY_CREDIT',
            'FEES': 'SELECT_BY_FEES',
            'DEFAULT': 'SELECT_BY_DEFAULT'
        }
        url = {
            SelectQuery.identifier: '/clients/wallets',
            'SELECT_CLIENT_WALLET': '/clients/wallets/%(fund_type)s/%(currency)s',
            'SELECT_BY_CREDIT': '/clients/wallets/CREDIT',
            'SELECT_BY_FEES': '/clients/wallets/FEES',
            'SELECT_BY_DEFAULT': '/clients/wallets'
        }

    def __str__(self):
        return 'Client wallet n.%s' % self.id

    @classmethod
    def get(cls, funds_type, currency, **kwargs):
        kwargs['fund_type'], kwargs['currency'] = funds_type, currency
        args = '',
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'SELECT_CLIENT_WALLET'
        return select.get(*args, **kwargs)

    @classmethod
    def all_by_funds_type(cls, fund_type, *args, **kwargs):
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = cls._meta.fund_type_url[fund_type]
        return select.all(*args, **kwargs)

    def get_pk(self):
        return getattr(self, 'id', None)

class RecurringPayInCIT(PayIn):
    recurring_payin_registration_id = CharField(api_name='RecurringPayinRegistrationId', required=True)
    browser_info = BrowserInfoField(api_name='BrowserInfo', required=True)
    ip_address = CharField(api_name='IpAddress', required=True)
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')
    author = ForeignKeyField(User, api_name='AuthorId')
    billing = BillingField(api_name='Billing')
    card = ForeignKeyField(Card, api_name='CardId')
    creation_date = DateTimeField(api_name='CreationDate')
    culture = CharField(api_name='Culture')
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    shipping = ShippingField(api_name='Shipping')

    def get_read_only_properties(self):
        read_only = ["AuthorId", "Applied3DSVersion", "CardId", "CreationDate", "Culture", "SecureModeNeeded"
            , "SecureMode", "SecureModeRedirectURL", "SecurityInfo"]
        return read_only

    class Meta:
        verbose_name = 'recurring_payin'
        verbose_name_plural = 'recurring_payins'
        url = {
            InsertQuery.identifier: '/payins/recurring/card/direct',
            SelectQuery.identifier: '/payins'
        }

class RecurringPayInMIT(PayIn):
    recurring_payin_registration_id = CharField(api_name='RecurringPayinRegistrationId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    browser_info = BrowserInfoField(api_name='BrowserInfo')
    ip_address = CharField(api_name='IpAddress')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')
    author = ForeignKeyField(User, api_name='AuthorId')
    billing = BillingField(api_name='Billing')
    card = ForeignKeyField(Card, api_name='CardId')
    creation_date = DateTimeField(api_name='CreationDate')
    culture = CharField(api_name='Culture')
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    shipping = ShippingField(api_name='Shipping')

    def get_read_only_properties(self):
        read_only = ["AuthorId", "Applied3DSVersion", "CardId", "CreationDate", "Culture", "SecureModeNeeded"
            , "SecureMode", "SecureModeRedirectURL", "SecurityInfo", "DebitedFunds", "Fees",
                     "StatementDescriptor", "BrowserInfo", "IpAddress", "SecureModeReturnURL"]
        return read_only

    class Meta:
        verbose_name = 'recurring_payin'
        verbose_name_plural = 'recurring_payins'
        url = {
            InsertQuery.identifier: '/payins/recurring/card/direct',
            SelectQuery.identifier: '/payins'
        }


class DirectPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    creation_date = DateTimeField(api_name='CreationDate')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    billing = BillingField(api_name='Billing')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    culture = CharField(api_name='Culture')
    ip_address = CharField(api_name='IpAddress')
    browser_info = BrowserInfoField(api_name='BrowserInfo')
    shipping = ShippingField(api_name='Shipping')
    requested_3ds_version = CharField(api_name='Requested3DSVersion')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/card/direct',
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Direct Payin: %s to %s' % (self.author_id, self.credited_user_id)

class CardWebPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    return_url = CharField(api_name='ReturnURL')
    template_url_options = CharField(api_name='TemplateURLOptions')
    culture = CharField(api_name='Culture')
    card_type = CharField(api_name='CardType', choices=constants.CARD_TYPE_CHOICES, default=None)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    redirect_url = CharField(api_name='RedirectURL')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    shipping = ShippingField(api_name='Shipping')

    class Meta:
        verbose_name = 'card_payin'
        verbose_name_plural = 'card_payins'
        url = {
            InsertQuery.identifier: '/payins/card/web',
            SelectQuery.identifier: '/payins'
        }

class Mandate(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', related_name='mandates')
    bank_account_id = CharField(api_name='BankAccountId', required=True)
    return_url = CharField(api_name='ReturnURL')
    redirect_url = CharField(api_name='RedirectURL')
    document_url = CharField(api_name='DocumentURL')
    culture = CharField(api_name='Culture')
    bank_reference = CharField(api_name='BankReference')

    scheme = CharField(api_name='Scheme', choices=constants.MANDATE_SCHEME_CHOICES, default=None)

    status = CharField(api_name='Status',
                       choices=constants.MANDATE_STATUS_CHOICES,
                       default=None)

    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    mandate_type = CharField(api_name='MandateType', choiced=constants.MANDATE_TYPE_CHOICES, default=None)

    creation_date = DateTimeField(api_name='CreationDate')

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'MANDATE_GET_TRANSACTIONS'
        return select.all(*args, **kwargs)

    class Meta:
        verbose_name = 'mandate'
        verbose_name_plural = 'mandates'
        url = {
            SelectQuery.identifier: '/mandates',
            InsertQuery.identifier: '/mandates/directdebit/web',
            'CANCEL_MANDATE': '/mandates/%(id)s/cancel/',
            'MANDATES_FOR_BANKACCOUNT': '/users/%(user_id)s/bankaccounts/%(id)s/mandates/'
        }

    def __str__(self):
        return 'Mandate n.%s' % self.id

    def cancel(self, handler=None):
        self._handler = handler or self.handler

        if self.status not in ('SUBMITTED', 'ACTIVE'):
            raise TypeError('Mandate status must be SUBMITTED or ACTIVE')

        action = ActionQuery(
            Mandate,
            self.get_pk(),
            'CANCEL_MANDATE'
        )
        return action.execute(handler)

class DirectDebitDirectPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    mandate = ForeignKeyField(Mandate, api_name='MandateId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')
    charge_date = CharField(api_name='ChargeDate')
    culture = CharField(api_name='Culture')

    class Meta:
        verbose_name = 'direct_debit_direct_payin'
        verbose_name_plural = 'direct_debit_direct_payins'
        url = {
            InsertQuery.identifier: '/payins/directdebit/direct',
            SelectQuery.identifier: '/payins'
        }

class DirectDebitWebPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    return_url = CharField(api_name='ReturnURL')
    template_url_options = CharField(api_name='TemplateURLOptions')
    culture = CharField(api_name='Culture')
    direct_debit_type = CharField(api_name='DirectDebitType', choices=constants.DIRECT_DEBIT_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    redirect_url = CharField(api_name='RedirectURL')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)

    class Meta:
        verbose_name = 'direct_debit_payin'
        verbose_name_plural = 'direct_debit_payins'
        url = {
            InsertQuery.identifier: '/payins/directdebit/web',
            SelectQuery.identifier: '/payins'
        }

class PreAuthorizedPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    preauthorization = ForeignKeyField(PreAuthorization, api_name='PreauthorizationId', required=True)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    culture = CharField(api_name='Culture')

    class Meta:
        verbose_name = 'preauthorized_payin'
        verbose_name_plural = 'preauthorized_payins'
        url = {
            InsertQuery.identifier: '/payins/PreAuthorized/direct',
            SelectQuery.identifier: '/payins'
        }

class BankWirePayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    declared_debited_funds = MoneyField(api_name='DeclaredDebitedFunds', required=True)
    declared_fees = MoneyField(api_name='DeclaredFees', required=True)
    wire_reference = CharField(api_name='WireReference')
    bank_account = CharField(api_name='BankAccount')
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/bankwire/direct',
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Bank Wire Payin: %s to %s' % (self.author_id, self.credited_user_id)

class BankWirePayInExternalInstruction(PayIn):
    banking_alias_id = CharField(api_name='BankingAliasId')
    wire_reference = CharField(api_name='WireReference')
    debited_bank_account = DebitedBankAccountField(api_name='DebitedBankAccount')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Bank Wire Payin External Instruction'

class ApplepayPayIn(PayIn):
    tag = CharField(api_name='Applepay PayIn')
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    payment_data = ApplepayPaymentDataField(api_name='PaymentData', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')

    class Meta:
        verbose_name = 'applepay_payin'
        verbose_name_plural = 'applepay_payins'
        url = {
            InsertQuery.identifier: '/payins/applepay/direct'
        }


class GooglepayPayIn(PayIn):
    tag = CharField(api_name='Googlepay PayIn')
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    payment_type = GooglepayPaymentDataField(api_name='PaymentData', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')

    class Meta:
        verbose_name = 'googlepay_payin'
        verbose_name_plural = 'googlepay_payins'
        url = {
            InsertQuery.identifier: '/payins/googlepay/direct'
        }
#######ANTON#######ANTON
class Clients(models.Model):
    OPTION_ONE_ADDRESS='HeadquartersAddress.AddressLine1'
    OPTION_TWO_ADDRESS='HeadquartersAddress.AddressLine2'
    OPTION_THREE_ADDRESS='HeadquartersAddress.City'
    OPTION_FOUR_ADDRESS = 'HeadquartersAddress.Region'
    OPTION_FIVE_ADDRESS='HeadquartersAddress.PostalCode'
    OPTION_SIX_ADDRESS='HeadquartersAddress.Country'
    OPTION_CHOICES_ADDRESS=[
        (OPTION_ONE_ADDRESS, 'Address One'),
         (OPTION_TWO_ADDRESS, 'Address Two'),
         (OPTION_THREE_ADDRESS, 'City'),
         (OPTION_FOUR_ADDRESS, 'Region'),
         (OPTION_FIVE_ADDRESS, 'Postal Code'),
         (OPTION_SIX_ADDRESS, 'Country')]
  
    OPTION_ONE='PlatformCategorization.BusinessType'
    OPTION_TWO='PlatformCategorization.Sector'
    OPTION_CHOICES=[
        (OPTION_ONE, 'Option One'),
         (OPTION_TWO, 'Option Two')]

    name= models.TextField()
    RegisteredNamestring = models.TextField()
    ClientId = models.TextField()
    PrimaryThemeColour= models.CharField(max_length=7)
    PrimaryButtonColour= models.CharField(max_length=7)
    Logos= models.TextField()
    TechEmails=models.CharField(max_length=255, blank=True, null=True, verbose_name='Admin/Commercial Contact Emails', help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.') #lista
    AdminEmails=models.CharField(max_length=255, blank=True, null=True, verbose_name='Admin/Commercial Contact Emails', help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.') #lista
    FraudEmails= models.CharField(max_length=255, blank=True, null=True, verbose_name='Admin/Commercial Contact Emails', help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.') #lista
    Billing_Emails = models.CharField(max_length=255, blank=True, null=True, verbose_name='Admin/Commercial Contact Emails', help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.') #lista
    PlatformCategorization= models.CharField(max_length=100,choices= OPTION_CHOICES)
    PlatformDescription=models.TextField()
    PlatformURL = models.TextField()
    HeadquartersAddress= models.CharField(max_length=100,choices= OPTION_CHOICES_ADDRESS)
    TaxNumber=models.TextField()
    CompanyReference = models.CharField(max_length=100)

class PayInobject(models.Model):
    PaymentTypePayIn=models.CharField(choices='PAYIN_PAYMENT_TYPE')
    ExecutionType = models.CharField(choices='EXECUTION_TYPE_CHOICES')



    #######ANTON#######ANTON
