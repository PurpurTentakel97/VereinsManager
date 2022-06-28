# Purpur Tentakel
# 14.04.2022
# VereinsManager / Member Entry Letter PDF

import datetime
import sys

from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate, Paragraph, FrameBreak, Spacer

from logic.pdf_handler.base_pdf import BasePDF

from helpers import validation, helper
from config import exception_sheet as e, config_sheet as c
from logic.main_handler import member_handler, organisation_handler, user_handler, log_handler
import debug

debug_str: str = "MemberEntryLetterPDF"

member_entry_letter_pdf: "MemberEntryLetterPDF"


class MemberEntryLetterPDF(BasePDF):
    def __init__(self) -> None:
        super().__init__()

        self.member_data: dict = dict()  # is filled in get_data
        self.organisation_data = dict()  # is filled in get_data
        self.contact_person_data: dict = dict()  # is filled in get_data
        self.current_user_data: dict = dict()  # is filled in get_data
        self.log_data: dict = dict()  # is filled in get_data

    def create_pdf(self, ID: int, path: str, active: bool, log_id: int) -> tuple[str | None, bool]:
        try:
            validation.must_positive_int(int_=ID, max_length=None)
            validation.must_str(str_=path, length=None)
            validation.must_bool(bool_=active)
            validation.must_positive_int(int_=log_id, max_length=None)
        except e.InputError as error:
            debug.info(item=debug_str, keyword=f"create_pdf", error_=sys.exc_info())
            return error.message, False

        self.create_basics(path=path)
        doc: SimpleDocTemplate = self._get_doc()
        frames: dict = self._get_frames(doc=doc)
        result, valid = self._get_data(ID=ID, active=active, log_id=log_id)
        if not valid:
            return result, valid

        try:
            validation.check_member_entry_letter_export(log_data=self.log_data)
        except e.InputError as error:
            debug.info(item=debug_str, keyword=f"create_pdf", error_=sys.exc_info())
            return error.message, False

        letter_key: str = self._get_letter_key()

        doc.addPageTemplates(PageTemplate(id='frames', frames=[x[1] for x in frames.items()]))

        elements = self._get_elements(letter_key=letter_key)

        return self._export(doc=doc, elements=elements, numbered=False)

    def _get_data(self, ID: int, active: bool, log_id: int) -> tuple[None | str, bool]:
        member_data, valid = member_handler.get_member_data(ID=ID, active=active)
        if not valid:
            return member_data, valid
        self.member_data = member_data['member_data']

        self.organisation_data, valid = organisation_handler.get_organisation_data()
        if not valid:
            return self.organisation_data, valid

        self.contact_person_data, valid = user_handler.get_data_of_user_by_ID(
            ID=int(self.organisation_data['contact_person'][0]), active=True)
        if not valid:
            return self.contact_person_data, valid

        self.current_user_data, valid = user_handler.get_data_of_user_by_ID(ID=c.config.user.ID, active=True)
        if not valid:
            return self.current_user_data, valid

        self.log_data, valid = log_handler.get_log_by_ID(ID=log_id)
        if not valid:
            return self.log_data, valid

        return None, True

    @staticmethod
    def _get_frames(doc: SimpleDocTemplate) -> dict:
        header: float = 3 * cm  # height
        address: float = 4 * cm  # height
        side_bar: float = 5.5 * cm  # with
        footer: float = 1 * cm  # height
        return {
            "header": Frame(
                x1=doc.leftMargin,
                y1=doc.bottomMargin + doc.height - header,
                width=doc.width - side_bar,
                height=header
            ),
            "address": Frame(
                x1=doc.leftMargin,
                y1=doc.bottomMargin + doc.height - header - address,
                width=doc.width - side_bar,
                height=address
            ),
            "main": Frame(
                x1=doc.leftMargin,
                y1=doc.bottomMargin + footer,
                width=doc.width - side_bar,
                height=doc.height - footer - header - address
            ),
            "side_bar": Frame(
                x1=doc.leftMargin + doc.width - side_bar,
                y1=doc.bottomMargin + footer,
                width=side_bar,
                height=doc.height - footer
            ),
            "footer": Frame(
                x1=doc.leftMargin,
                y1=doc.bottomMargin,
                width=doc.width,
                height=footer
            ),
        }

    def _get_elements(self, letter_key: str) -> list:
        elements: list = list()
        elements.extend(self._get_header_data())
        elements.append(FrameBreak())
        elements.extend(self._get_address_data())
        elements.append(FrameBreak())
        elements.extend(self._get_main_data(letter_key=letter_key))
        elements.append(FrameBreak())
        elements.extend(self._get_sidebar_data())
        elements.append(FrameBreak())
        elements.extend(self._get_footer_data())
        return elements

    def _get_letter_key(self) -> str:
        match self.log_data['target_column']:
            case 'membership_type':
                return c.config.letters.keys['chance']
            case 'active':
                if self.log_data['new_data']:
                    return c.config.letters.keys['entry']
                return c.config.letters.keys['exit']

    def _get_header_data(self) -> list:
        elements: list = [
            Spacer(0, 0.5 * cm),
            Paragraph(helper.try_transform_to_None_string(string=self.organisation_data['name']),
                      style=self.style_sheet['Title']),
        ]

        return elements

    def _get_address_data(self) -> list:
        elements: list = [
            Paragraph(f"{helper.try_transform_to_None_string(string=self.organisation_data['name'])}<br/>"
                      f"{helper.combine_strings(strings=(self.current_user_data['firstname'], self.current_user_data['lastname']))} / "
                      f"{helper.combine_strings(strings=(self.current_user_data['street'], self.current_user_data['number']))} / "
                      f"{helper.combine_strings(strings=(self.current_user_data['zip_code'], self.current_user_data['city']))} / "
                      f"{helper.try_transform_to_None_string(string=self.current_user_data['phone'])} / "
                      f"{helper.try_transform_to_None_string(string=self.current_user_data['mail'])}",
                      style=self.custom_styles['CustomBodyTextSmall']),
            Spacer(0, 0.5),
            Paragraph(
                f"<b>{helper.combine_strings(strings=(self.member_data['first_name'], self.member_data['last_name']))}</b><br/>"
                f"<b>{helper.combine_strings(strings=(self.member_data['street'], self.member_data['number']))}</b><br/>"
                f"<b>{helper.combine_strings(strings=(self.member_data['zip_code'], self.member_data['city']))}</b><br/>"
                f"<b>{helper.try_transform_to_None_string(string=self.member_data['country'])}</b>",
                style=self.style_sheet['BodyText']),
        ]
        return elements

    def _get_main_data(self, letter_key: str) -> list:
        main_text: str = self._get_main_text(letter_key=letter_key)
        info_text: str = self._get_info_text(letter_key=letter_key)

        elements: list = [
            Paragraph(datetime.datetime.strftime(datetime.datetime.now(), c.config.date_format.short),
                      style=self.style_sheet['BodyText']),
            Spacer(0, 1.5 * cm),
            Paragraph(f"<b>{helper.try_transform_to_None_string(string=c.config.letters.text[letter_key])}</b>",
                      style=self.style_sheet['BodyText']),
            Spacer(0, 0.5 * cm),
            Paragraph(helper.try_transform_to_None_string(string=main_text), style=self.style_sheet['BodyText']),
            Spacer(0, 3 * cm),
            Paragraph(f"{'_' * 40}<br/>"
                      f"{helper.combine_strings(strings=(self.current_user_data['firstname'], self.current_user_data['lastname']))}<br/>"
                      f"{helper.try_transform_to_None_string(string=self.current_user_data['position'])}",
                      self.custom_styles['CustomBodyTextSmallCenter']),
            Spacer(0, 3 * cm),
            Paragraph("<b>Informationen:</b>", style=self.style_sheet['BodyText']),
            Paragraph(helper.try_transform_to_None_string(string=info_text), style=self.style_sheet['BodyText']),

        ]

        return elements

    def _get_sidebar_data(self) -> list:
        elements: list = list()
        if self._is_icon():
            elements.append(self._get_icon('letter'))
            elements.append(Spacer(0, 0.5 * cm))

        elements.extend([
            Paragraph(f"{helper.try_transform_to_None_string(string=self.organisation_data['name'])}<br/>"
                      f"{helper.combine_strings(strings=(self.organisation_data['street'], self.organisation_data['number']))}<br/>"
                      f"{helper.combine_strings(strings=(self.organisation_data['zip_code'], self.organisation_data['city']))}<br/>"
                      f"{helper.try_transform_to_None_string(string=self.organisation_data['country'])}<br/>"
                      f"{helper.try_transform_to_None_string(string=self.organisation_data['web_link'])}",
                      self.style_sheet['BodyText']),
            Spacer(0, 0.5 * cm),
            Paragraph(f"{helper.try_transform_to_None_string(string=self.contact_person_data['position'])}<br/>"
                      f"{helper.combine_strings(strings=(self.contact_person_data['firstname'], self.contact_person_data['lastname']))}<br/>"
                      f"{helper.combine_strings(strings=(self.contact_person_data['street'], self.contact_person_data['number']))}<br/>"
                      f"{helper.combine_strings(strings=(self.contact_person_data['zip_code'], self.contact_person_data['city']))}<br/>"
                      f"{helper.try_transform_to_None_string(string=self.contact_person_data['country'])}<br/>"
                      f"{helper.try_transform_to_None_string(string=self.contact_person_data['phone'])}<br/>"
                      f"{helper.try_transform_to_None_string(string=self.contact_person_data['mail'])}<br/>",
                      self.style_sheet['BodyText']),
            Spacer(0, 0.5 * cm),
            Paragraph(helper.try_transform_to_None_string(string=self._get_extra_text()), self.style_sheet['BodyText'])
        ])

        return elements

    def _get_footer_data(self) -> list:
        elements: list = [
            Paragraph(
                f"Bankverbindung: {helper.try_transform_to_None_string(string=self.organisation_data['bank_name'])} "
                f"IBAN: {helper.try_transform_to_None_string(string=self.organisation_data['bank_IBAN'])} "
                f"BIC: {helper.try_transform_to_None_string(string=self.organisation_data['bank_BIC'])}",
                self.custom_styles['CustomBodyTextSmallCenter']),
        ]
        return elements

    def _get_main_text(self, letter_key: str) -> str:
        date = datetime.datetime.strftime(self.log_data['log_date'], c.config.date_format.short)

        main_text: str = c.config.letters.text[letter_key]
        main_text = main_text.replace("<member_name>", helper.combine_strings(strings=(self.member_data['first_name'],
                                                                                       self.member_data['last_name'])))
        main_text = main_text.replace("<date>", date)
        main_text = main_text.replace("<organisation_name>",
                                      f'"{helper.try_transform_to_None_string(string=self.organisation_data["name"])}"')
        try:
            main_text = main_text.replace("<old_membership_type>",
                                          helper.try_transform_to_None_string(string=self.log_data['old_data']))
            main_text = main_text.replace("<new_membership_type>",
                                          helper.try_transform_to_None_string(string=self.log_data['new_data']))
        except TypeError:
            pass

        return main_text

    def _get_info_text(self, letter_key: str) -> str:
        info_text: str = c.config.letters.info[letter_key]
        info_text = info_text.replace("<membership_type>",
                                      helper.try_transform_to_None_string(string=self.member_data['membership_type']))
        info_text = info_text.replace("<amount>", helper.try_transform_to_None_string(
            string=self.member_data['membership_type_extra_value']))

        return info_text

    def _get_extra_text(self) -> str:
        extra_text: str = helper.try_transform_to_None_string(string=self.organisation_data['extra_text'])
        extra_text = extra_text.replace("\n", "<br/>")
        return extra_text


def create() -> None:
    global member_entry_letter_pdf
    member_entry_letter_pdf = MemberEntryLetterPDF()
