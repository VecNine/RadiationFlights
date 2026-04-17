# RadiationFlights


# RadiationFlights - Mapowanie Danych

| Twoja Dana (JSON) | Odpowiednik OMNI NASA | Wyjaśnienie / Rola w modelu |
| :--- | :--- | :--- |
| **Datetime** | Time | Klucz czasowy do połączenia obu baz. |
| **ARMAS** | NaN | Cel predykcji (Target). Rzeczywista dawka w samolocie. |
| **Latitude / Longitude** | NaN | Pozycja geograficzna (kluczowa dla grubości atmosfery). |
| **Altitude (Bar/GPS)** | NaN | Wysokość lotu (najsilniejszy czynnik radiacji). |
| **Geomagnetic_Rc** | NaN | Sztywność odcięcia (obliczana na podstawie pozycji). |
| **Index_Kp (30.0)** | KP1800 (30) | Globalny stan burzy magnetycznej (skala *10). |
| **Index_Dst (-4.0)** | DST1800 (-4) | Stopień ugięcia ziemskiej tarczy magnetycznej. |
| **Index_Ap** | AP_INDEX1800 | Liniowy odpowiednik Kp (często używany w lotnictwie). |
| **Solar_sunspots** | R1800 | Liczba plam słonecznych (faza cyklu słonecznego). |
| **Solar_f107** | F10_INDEX1800 | Aktywność radiowa korony słonecznej. |
| **SW_B (11.88)** | ABS_B1800 | Całkowita siła międzyplanetarnego pola magnetycznego. |
| **SW_Bz (10.76)** | BZ_GSM1800 | Składowa "północ-południe" pola (klucz do "otwarcia" tarczy). |
| **SW_V (417.2)** | V1800 | Prędkość wiatru słonecznego (km/s). |
| **SW_density (4.37)** | N1800 | Gęstość cząstek (liczba protonów na cm3). |
| **SW_temperature** | T1800 | Temperatura plazmy słonecznej. |
| **SW_pressure** | Pressure1800 | Ciśnienie wiatru słonecznego na magnetosferę. |
| **Particles_P10** | PR-FLX_101800 | Strumień protonów o wysokiej energii (> 10 MeV). |
| **Particles_P30** | PR-FLX_301800 | Strumień protonów o wysokiej energii (> 30 MeV). |
| **Particles_P60** | PR-FLX_601800 | Strumień protonów o wysokiej energii (> 60 MeV). |
| **NM_OULU / NM_THUL** | NaN | Pomiary naziemne neutronów (inne źródło danych). |
| **SXR_short / long** | NaN | Promieniowanie X ze Słońca (zazwyczaj z satelitów GOES). |
| **Geomagnetic_Lshell** | NaN | Parametr budowy pola magnetycznego w danym punkcie. |



Krótka odpowiedź brzmi: Większość kluczowych parametrów ma te same jednostki, ale jest kilka pułapek, na które musisz uważać, aby Twój model nie otrzymał błędnych informacji.

Oto szczegółowe porównanie jednostek w obu bazach:

1. Indeksy magnetyczne (Zgodne, ale specyficzne)

Parametr	Jednostka w Twoim JSON	Jednostka w OMNI	Uwagi
Kp Index	Skala 0−90 (np. 30.0)	Skala 0−90 (np. 57)	To jest to samo. Obie bazy używają konwencji Kp×10. Jeśli chcesz skali 0−9, musisz podzielić przez 10.
Dst Index	nT (nanotesle)	nT (nanotesle)	Pełna zgodność. Wartości ujemne oznaczają burzę.
Ap Index	nT	nT	Pełna zgodność.
2. Słońce i Wiatr Słoneczny (Głównie zgodne)

Parametr	Jednostka w Twoim JSON	Jednostka w OMNI	Uwagi
f10.7 Index	SFU	SFU	Jednostka strumienia radiowego (10 
−22
  W m 
−2
  Hz 
−1
 ). Pełna zgodność.
Prędkość (V)	km/s	km/s	Pełna zgodność.
Gęstość (N)	n/cm 
3
 	n/cm 
3
 	Liczba protonów na centymetr sześcienny. Pełna zgodność.
Temperatura	K (Kelwiny)	K (Kelwiny)	Pełna zgodność.
Ciśnienie	nPa (nanopaskale)	nPa (nanopaskale)	W OMNI2 ciśnienie jest podawane jako P=2⋅10 
−6
 ⋅N⋅V 
2
 . Jednostki powinny się zgadzać.
3. Cząstki i Protony (GŁÓWNA RÓŻNICA)

Tutaj musisz zachować czujność. Twoje dane Particles_P10 i OMNI PR-FLX_10 mogą mieć inne skale:

Twoje dane: Zazwyczaj pochodzą bezpośrednio z satelitów GOES i są to tzw. Integral Flux (strumień całkowy).

OMNI: Często stosuje uśrednianie lub inne progi detekcji.

Rekomendacja: Zanim wrzucisz te dane do jednego worka w modelu, narysuj wykres (np. w Matplotlib) dla tego samego okresu dla obu baz. Jeśli Twoje dane to 0.07, a OMNI to 0.15, oznacza to, że mają inne skalowanie i model powinien uczyć się na jednej, spójnej kolumnie (lepiej wybrać tę z OMNI, bo jest pełniejsza).
