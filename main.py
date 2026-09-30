import math
import os
import urllib.request
import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# تنزيل خط عربي داعم
FONT_PATH = "Amiri-Regular.ttf"
if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
    try:
        urllib.request.urlretrieve(font_url, FONT_PATH)
    except Exception as e:
        print("خطأ في تنزيل الخط:", e)

def ar(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

class BonusCalculatorApp(App):
    def build(self):
        self.title = "حاسبة مكافآت ومؤشر الكفاءة"
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=6)
        
        # خلفية سماوي فاتح
        with main_layout.canvas.before:
            Color(0.85, 0.93, 0.98, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # العنوان الرئيسي
        header = Label(
            text=f"[b]{ar('حاسبة المكافآت ومؤشر الكفاءة الأوروبي')}[/b]", 
            markup=True, 
            font_size='18sp', 
            font_name=FONT_PATH,
            size_hint_y=None, 
            height=35, 
            color=(0.05, 0.15, 0.35, 1)
        )
        main_layout.add_widget(header)

        # حقول الإدخال
        self.input_salary = self.create_input("الراتب الأساسي (جنيه):")
        self.input_feed = self.create_input("إجمالي العلف المستهلك (كجم):")
        self.input_weight_after = self.create_input("الوزن بعد تصفية السردة [لـ FCR] (كجم):")
        self.input_weight_before = self.create_input("الوزن قبل تصفية السردة [لمعامل اللحم] (كجم):")
        self.input_birds = self.create_input("العدد المستلم (كتكوت):")
        self.input_mortality = self.create_input("إجمالي النافق (طائر):")
        self.input_age = self.create_input("عمر الطيور عند البيع (يوم):")

        main_layout.add_widget(self.input_salary[0])
        main_layout.add_widget(self.input_feed[0])
        main_layout.add_widget(self.input_weight_after[0])
        main_layout.add_widget(self.input_weight_before[0])
        main_layout.add_widget(self.input_birds[0])
        main_layout.add_widget(self.input_mortality[0])
        main_layout.add_widget(self.input_age[0])

        # زر الحساب
        btn_calc = Button(
            text=ar("احسب النتائج الآن"), 
            font_size='16sp', 
            font_name=FONT_PATH,
            bold=True,
            size_hint_y=None, 
            height=40, 
            background_color=(0.1, 0.5, 0.2, 1), 
            color=(1, 1, 1, 1)
        )
        btn_calc.bind(on_press=self.calculate)
        main_layout.add_widget(btn_calc)

        # عرض النتائج
        scroll = ScrollView(size_hint=(1, 1))
        self.label_result = Label(
            text=ar("أدخل البيانات واضغط احسب"), 
            font_size='13sp',
            font_name=FONT_PATH,
            color=(0.05, 0.1, 0.25, 1),
            size_hint_y=None,
            halign='right', 
            valign='top'
        )
        self.label_result.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.label_result.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        scroll.add_widget(self.label_result)
        main_layout.add_widget(scroll)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def create_input(self, label_text):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=46)
        lbl = Label(
            text=ar(label_text), 
            font_size='11sp', 
            font_name=FONT_PATH,
            color=(0.05, 0.2, 0.4, 1), 
            size_hint_y=None, 
            height=16, 
            halign='right'
        )
        lbl.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        inp = TextInput(
            multiline=False, 
            input_filter='float', 
            input_type='number',
            base_direction='ltr',
            write_tab=False,
            halign='center', 
            font_size='13sp',
            foreground_color=(0, 0, 0, 1)
        )
        box.add_widget(lbl)
        box.add_widget(inp)
        return box, inp

    def calculate(self, instance):
        try:
            salary = float(self.input_salary[1].text)
            feed = float(self.input_feed[1].text)
            weight_after = float(self.input_weight_after[1].text)
            weight_before = float(self.input_weight_before[1].text)
            birds = float(self.input_birds[1].text)
            mortality = float(self.input_mortality[1].text if self.input_mortality[1].text else 0)
            age = float(self.input_age[1].text)

            if weight_before <= 0 or weight_after <= 0 or birds <= 0 or age <= 0:
                self.label_result.text = ar("برجاء إدخال أرقام صحيحة أكبر من الصفر.")
                return

            fcr = feed / weight_after
            meat_factor = weight_before / birds
            
            # 1. حسابات مؤشر الكفاءة الأوروبي (EPI)
            sold_birds = birds - mortality
            viability = (sold_birds / birds) * 100 if birds > 0 else 0
            avg_weight = weight_before / sold_birds if sold_birds > 0 else 0
            epi = (viability * avg_weight) / (age * fcr) * 100 if (age * fcr) > 0 else 0

            # تقييم مؤشر EPI
            if epi >= 400:
                epi_rating = "ممتاز جداً"
            elif epi >= 350:
                epi_rating = "جيد جداً"
            elif epi >= 300:
                epi_rating = "جيد"
            else:
                epi_rating = "ضعيف"

            # 2. حسابات شرائح المكافأة
            if 1.40 <= fcr <= 1.45:
                base_percent = 3.00
                level = "المستوى 1 (300%)"
                target_weight = 2.300
            elif 1.46 <= fcr <= 1.50:
                base_percent = 2.50
                level = "المستوى 2 (250%)"
                target_weight = 2.200
            elif 1.51 <= fcr <= 1.55:
                base_percent = 2.00
                level = "المستوى 3 (200%)"
                target_weight = 2.100
            elif 1.56 <= fcr <= 1.60:
                base_percent = 1.50
                level = "المستوى 4 (150%)"
                target_weight = 2.000
            elif 1.61 <= fcr <= 1.65:
                base_percent = 1.00
                level = "المستوى 5 (100%)"
                target_weight = 1.900
            elif 1.66 <= fcr <= 1.70:
                base_percent = 0.50
                level = "المستوى 6 (50%)"
                target_weight = 1.800
            else:
                base_percent = 0.00
                level = "خارج الشرائح"
                target_weight = None

            if base_percent == 0:
                res_text = (
                    f"FCR: {fcr:.3f}\n"
                    f"مؤشر الكفاءة الأوروبي (EPI): {epi:.1f} ({epi_rating})\n"
                    f"نسبة النافق: {(mortality/birds)*100:.1f}%\n"
                    f"----------------------------\n"
                    f"لا توجد مكافأة لارتفاع معامل التحويل."
                )
                self.label_result.text = ar(res_text)
                return

            min_stable = target_weight - 0.050
            max_stable = target_weight + 0.050

            adjust = 0.0
            note = f"داخل نطاق الثبات ({min_stable:.3f} - {max_stable:.3f} كجم)"

            if meat_factor > max_stable:
                steps = math.floor((meat_factor - max_stable) / 0.050)
                adjust = steps * 0.10
                note = f"زيادة وزن (+{int(adjust * 100)}%)"
            elif meat_factor < min_stable:
                steps = math.floor((min_stable - meat_factor) / 0.050)
                adjust = -(steps * 0.10)
                note = f"نقص وزن ({int(adjust * 100)}%)"

            final_percent = max(0.0, base_percent + adjust)
            bonus = salary * final_percent

            res_text = (
                f"مؤشر الكفاءة الأوروبي (EPI): {epi:.1f} ({epi_rating})\n"
                f"نسبة الحيوية: {viability:.1f}% | النافق: {int(mortality)}\n"
                f"معامل التحويل (FCR): {fcr:.3f} ({level})\n"
                f"معامل اللحم: {meat_factor:.3f} كجم\n"
                f"حالة الوزن: {note}\n"
                f"نسبة المكافأة النهائية: {int(final_percent * 100)}%\n"
                f"----------------------------\n"
                f"قيمة المكافأة: {bonus:,.2f} جنيه"
            )
            self.label_result.text = ar(res_text)

        except ValueError:
            self.label_result.text = ar("يرجى إدخال جميع البيانات بشكل صحيح.")

if __name__ == '__main__':
    BonusCalculatorApp().run()
