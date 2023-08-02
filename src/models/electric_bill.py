""" Electric Bills. """

from dataclasses import dataclass, field

from mashumaro import DataClassDictMixin, field_options
from response_descriptor import ResponseDescriptor


@dataclass
class Invoice(DataClassDictMixin):
    full_date: str = field(metadata=field_options(alias="fullDate"))
    from_date: str = field(metadata=field_options(alias="fromDate"))
    to_date: str = field(metadata=field_options(alias="toDate"))
    amount_origin: float = field(metadata=field_options(alias="amountOrigin"))
    amount_to_pay: float = field(metadata=field_options(alias="amountToPay"))
    amount_paid: float = field(metadata=field_options(alias="amountPaid"))
    invoice_id: int = field(metadata=field_options(alias="invoiceId"))
    contract_number: int = field(metadata=field_options(alias="contractNumber"))
    order_number: int = field(metadata=field_options(alias="orderNumber"))
    last_date: str = field(metadata=field_options(alias="lastDate"))
    invoice_payment_status: int = field(
        metadata=field_options(alias="invoicePaymentStatus")
    )
    document_id: str = field(metadata=field_options(alias="documentId"))
    days_period: str = field(metadata=field_options(alias="daysPeriod"))
    has_direct_debit: bool = field(metadata=field_options(alias="hasDirectDebit"))
    invoice_type: int = field(metadata=field_options(alias="invoiceType"))


@dataclass
class Invoices(DataClassDictMixin):
    total_amount_to_pay: float = field(metadata=field_options(alias="totalAmountToPay"))
    total_invoices_to_pay: int = field(
        metadata=field_options(alias="totalInvoicesToPay")
    )
    last_date_to_pay: str = field(metadata=field_options(alias="lastDateToPay"))
    invoices: list[Invoice]


@dataclass
class GetInvoicesResponse(DataClassDictMixin):
    data: Invoices
    response_descriptor: ResponseDescriptor = field(
        metadata=field_options(alias="responseDescriptor")
    )
