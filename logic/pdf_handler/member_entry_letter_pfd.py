# Purpur Tentakel
# 14.04.2022
# VereinsManager / Member Entry Letter PDF
import datetime
import sys

from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate, Paragraph, FrameBreak, Spacer

from logic.pdf_handler.base_pdf import BasePDF

from helper import validation
from config import exception_sheet as e, config_sheet as c
from logic.main_handler import member_handler, organisation_handler, user_handler, log_handler
import debug

debug_str: str = "MemberEntryLetterPDF"

member_entry_letter_pdf: "MemberEntryLetterPDF"


class MemberEntryLetterPDF(BasePDF):
    def __init__(self) -> None:
        super().__init__()

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
        data = self._get_data(ID=ID, active=active, log_id=log_id)
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data

        try:
            validation.check_member_entry_letter_export(log_data=log_data)
        except e.InputError as error:
            debug.info(item=debug_str, keyword=f"create_pdf", error_=sys.exc_info())
            return error.message, False

        letter_key: str = self._get_letter_key(log_data=log_data, active=active)

        doc.addPageTemplates(PageTemplate(id='frames', frames=[x[1] for x in frames.items()]))

        elements: list = list()
        elements.extend(self._get_header_data(data=data))
        elements.append(FrameBreak())
        elements.extend(self._get_address_data(data=data))
        elements.append(FrameBreak())
        elements.extend(self._get_main_data(data=data, letter_key=letter_key))
        elements.append(FrameBreak())
        elements.extend(self._get_sidebar_data(data=data))
        elements.append(FrameBreak())
        elements.extend(self._get_footer_data(data=data))

        return self._export(doc=doc, elements=elements, numbered=False)

    @staticmethod
    def _get_data(ID: int, active: bool, log_id: int) -> tuple:
        member_data, _ = member_handler.get_member_data(ID=ID, active=active)
        debug.debug(item=debug_str, keyword="_get_data", message=f"member_data = {member_data}")
        organisation_data, _ = organisation_handler.get_organisation_data()
        debug.debug(item=debug_str, keyword="_get_data", message=f"organisation_data = {organisation_data}")
        contact_person_data, _ = user_handler.get_data_of_user_by_ID(ID=organisation_data['contact_person'][0],
                                                                     active=True)
        debug.debug(item=debug_str, keyword="_get_data", message=f"contact_person_data = {contact_person_data}")
        current_user_data, _ = user_handler.get_data_of_user_by_ID(ID=c.config.user['ID'], active=True)
        log_data, _ = log_handler.get_log_by_ID(ID=log_id)
        debug.debug(item=debug_str, keyword="_get_data", message=f"log_data = {log_data}")

        return member_data, organisation_data, contact_person_data, current_user_data, log_data

    @staticmethod
    def _get_frames(doc: SimpleDocTemplate) -> dict:
        header = 3 * cm  # height
        address = 4 * cm  # height
        side_bar = 5.5 * cm  # with
        footer = 1 * cm  # height
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

    @staticmethod
    def _get_letter_key(log_data: dict, active: bool) -> str:
        match log_data['target_column']:
            case 'membership_type':
                return c.config.letters['keys']['chance']
            case 'active':
                if log_data['new_data']:
                    return c.config.letters['keys']['entry']
                return c.config.letters['keys']['exit']

    def _get_header_data(self, data: tuple) -> list:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data

        elements: list = [
            Spacer(0, 0.5 * cm),
            Paragraph(organisation_data['name'], style=self.style_sheet['Title']),
        ]

        return elements

    def _get_address_data(self, data: tuple) -> list:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data
        member_data = member_data['member_data']

        elements: list = [
            Paragraph(f"{organisation_data['name']}<br/>"
                      f"{self._get_combined_str(str_1=current_user_data['firstname'], str_2=current_user_data['lastname'])} / "
                      f"{self._get_combined_str(str_1=current_user_data['street'], str_2=current_user_data['number'])} / "
                      f"{self._get_combined_str(str_1=current_user_data['zip_code'], str_2=current_user_data['city'])} / "
                      f"{current_user_data['phone']} / "
                      f"{current_user_data['mail']}",
                      style=self.custom_styles['CustomBodyTextSmall']),
            Spacer(0, 0.5),
            Paragraph(
                f"<b>{self._get_combined_str(str_1=member_data['first_name'], str_2=member_data['last_name'])}</b><br/>"
                f"<b>{self._get_combined_str(str_1=member_data['street'], str_2=member_data['number'])}</b><br/>"
                f"<b>{self._get_combined_str(str_1=member_data['zip_code'], str_2=member_data['city'])}</b><br/>"
                f"<b>{member_data['country']}</b>",
                style=self.style_sheet['BodyText']),
        ]
        return elements

    def _get_main_data(self, data: tuple, letter_key: str) -> list:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data
        member_data = member_data['member_data']

        main_text: str = self._get_main_text(data=data, letter_key=letter_key)
        info_text: str = self._get_info_text(data=data, letter_key=letter_key)

        elements: list = [
            Paragraph(datetime.datetime.strftime(datetime.datetime.now(), c.config.date_format['short']),
                      style=self.custom_styles['CustomBodyTextRight']),
            Spacer(0, 1.5 * cm),
            Paragraph(f"<b>{c.config.letters['title'][letter_key]}</b>", style=self.style_sheet['BodyText']),
            Spacer(0, 0.5 * cm),
            Paragraph(main_text, style=self.style_sheet['BodyText']),
            Spacer(0, 3 * cm),
            Paragraph(f"{'_' * 40}<br/>"
                      f"{self._get_combined_str(str_1=current_user_data['firstname'], str_2=current_user_data['lastname'])}<br/>"
                      f"{current_user_data['position']}",
                      self.custom_styles['CustomBodyTextSmallCenter']),
            Spacer(0, 3 * cm),
            Paragraph("<b>Informationen:</b>", style=self.style_sheet['BodyText']),
            Paragraph(info_text, style=self.style_sheet['BodyText']),

        ]

        return elements

    def _get_sidebar_data(self, data: tuple) -> list:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data

        debug.debug(item=debug_str, keyword="_get_sidebar_data",
                    message=f"extra text = {organisation_data['extra_text']}")

        elements: list = list()
        if self._is_icon:
            elements.append(self._get_icon('letter'))
            elements.append(Spacer(0, 0.5 * cm))

        elements.extend([
            Paragraph(f"{organisation_data['name']}<br/>"
                      f"{self._get_combined_str(str_1=organisation_data['street'], str_2=organisation_data['number'])}<br/>"
                      f"{self._get_combined_str(str_1=organisation_data['zip_code'], str_2=organisation_data['city'])}<br/>"
                      f"{organisation_data['country']}<br/>"
                      f"{organisation_data['web_link']}",
                      self.style_sheet['BodyText']),
            Spacer(0, 0.5 * cm),
            Paragraph(f"{contact_person_data['position']}<br/>"
                      f"{self._get_combined_str(str_1=contact_person_data['firstname'], str_2=contact_person_data['lastname'])}<br/>"
                      f"{self._get_combined_str(str_1=contact_person_data['street'], str_2=contact_person_data['number'])}<br/>"
                      f"{self._get_combined_str(str_1=contact_person_data['zip_code'], str_2=contact_person_data['city'])}<br/>"
                      f"{contact_person_data['country']}<br/>"
                      f"{contact_person_data['phone']}<br/>"
                      f"{contact_person_data['mail']}<br/>",
                      self.style_sheet['BodyText']),
            Spacer(0, 0.5 * cm),
            Paragraph(self._get_extra_text(data=data), self.style_sheet['BodyText'])
        ])

        return elements

    def _get_footer_data(self, data: tuple) -> list:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data

        elements: list = [
            Paragraph(f"Bankverbindung: {organisation_data['bank_name']} "
                      f"IBAN: {organisation_data['bank_IBAN']} "
                      f"BIC: {organisation_data['bank_BIC']}",
                      self.custom_styles['CustomBodyTextSmallCenter']),
        ]
        return elements

    @staticmethod
    def _get_combined_str(str_1: str, str_2: str) -> str:
        if str_1 and str_2:
            return f"{str_1} {str_2}"
        elif str_1:
            return str_1
        elif str_2:
            return str_2

    def _get_main_text(self, data: tuple, letter_key: str) -> str:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data
        member_data = member_data['member_data']
        date = datetime.datetime.strftime(log_data['log_date'], c.config.date_format['short'])

        main_text: str = c.config.letters['text'][letter_key]
        main_text = main_text.replace("<member_name>", self._get_combined_str(str_1=member_data['first_name'],
                                                                              str_2=member_data['last_name']))
        main_text = main_text.replace("<date>", date)
        main_text = main_text.replace("<organisation_name>", f'"{organisation_data["name"]}"')
        try:
            main_text = main_text.replace("<old_membership_type>", log_data['old_data'])
            main_text = main_text.replace("<new_membership_type>", log_data['new_data'])
        except TypeError:
            pass

        return main_text

    @staticmethod
    def _get_info_text(data: tuple, letter_key: str) -> str:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data
        member_data = member_data['member_data']

        info_text: str = c.config.letters['info'][letter_key]
        info_text = info_text.replace("<membership_type>", member_data['membership_type'])
        info_text = info_text.replace("<amount>", member_data['membership_type_extra_value'])

        return info_text

    @staticmethod
    def _get_extra_text(data: tuple) -> str:
        member_data, organisation_data, contact_person_data, current_user_data, log_data = data

        extra_text: str = organisation_data['extra_text']
        extra_text = extra_text.replace("\n", "<br/>")
        return extra_text


def create() -> None:
    global member_entry_letter_pdf
    member_entry_letter_pdf = MemberEntryLetterPDF()
