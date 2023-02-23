# Generated by Django 4.1.7 on 2023-02-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('RegisteredNamestring', models.TextField()),
                ('ClientId', models.TextField()),
                ('PrimaryThemeColour', models.CharField(max_length=7)),
                ('PrimaryButtonColour', models.CharField(max_length=7)),
                ('Logos', models.TextField()),
                ('TechEmails', models.CharField(blank=True, help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.', max_length=255, null=True, verbose_name='Admin/Commercial Contact Emails')),
                ('AdminEmails', models.CharField(blank=True, help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.', max_length=255, null=True, verbose_name='Admin/Commercial Contact Emails')),
                ('FraudEmails', models.CharField(blank=True, help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.', max_length=255, null=True, verbose_name='Admin/Commercial Contact Emails')),
                ('Billing_Emails', models.CharField(blank=True, help_text='A comma-separated list of email addresses to use when contacting you for admin/commercial issues/communications.', max_length=255, null=True, verbose_name='Admin/Commercial Contact Emails')),
                ('PlatformCategorization', models.CharField(choices=[('PlatformCategorization.BusinessType', 'Option One'), ('PlatformCategorization.Sector', 'Option Two')], max_length=100)),
                ('PlatformDescription', models.TextField()),
                ('PlatformURL', models.TextField()),
                ('HeadquartersAddress', models.CharField(choices=[('HeadquartersAddress.AddressLine1', 'Address One'), ('HeadquartersAddress.AddressLine2', 'Address Two'), ('HeadquartersAddress.City', 'City'), ('HeadquartersAddress.Region', 'Region'), ('HeadquartersAddress.PostalCode', 'Postal Code'), ('HeadquartersAddress.Country', 'Country')], max_length=100)),
                ('TaxNumber', models.TextField()),
                ('CompanyReference', models.CharField(max_length=100)),
            ],
        ),
    ]
