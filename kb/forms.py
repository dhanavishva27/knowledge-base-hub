from django import forms


class CSVUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload CSV or Excel file",
        help_text="Supported formats: .csv and .xlsx"
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]

        allowed_extensions = [".csv", ".xlsx"]

        file_name = uploaded_file.name.lower()

        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                "Only CSV and XLSX files are supported."
            )

        return uploaded_file