#libraries
import utime
import machine

#Werte
ausgetrockneter_wert = 58000
fast_ausgetrockneter_wert = 45000
trockenwert = 40000
nasswert = 28000

#feuchtigkeitssensor
sensor = machine.ADC(26)

#Wasserpumpensteuerung
w_p = machine.Pin(18, machine.Pin.OUT, machine.Pin.PULL_DOWN)

#led für fehlermeldungen
led = machine.Pin(16, machine.Pin.OUT)
led.value(0)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#automatisierung
        
def giessen(p_feuchtigkeitslevel, p_anfang):
    
    if p_feuchtigkeitslevel >= trockenwert:
       
       #falls es sehr trocken ist, soll zweimal gegossen werden, sonst nicht
        
        if p_feuchtigkeitslevel >= fast_ausgetrockneter_wert:
            w_p.on()
            utime.sleep_ms(2000) #zweieinhalb sec gießen
            w_p.off()
            utime.sleep_ms(2000) # 300000 fünf min warten
            
        
        w_p.on()
        utime.sleep_ms(2500) #zweieinhalb sec gießen
        w_p.off()
        utime.sleep_ms(2500) # 300000 fünf min warten
        
    led.value(0)
    # wenn nicht gegossen worden ist, warnlampe einschalten
    akt_feuchtigkeitswert = sensor.read_u16()
    if akt_feuchtigkeitswert in range(p_feuchtigkeitslevel, trockenwert):
        led.value(1)
    
    
    #falls der sensor nicht richtig funktioniert
    led.value(0)   
    if p_feuchtigkeitslevel >= ausgetrockneter_wert or p_feuchtigkeitslevel <= nasswert:
        led.toggle()
    
    utime.sleep_ms(1000) # 86400000 einen tag warten bevor die fkt. nochmal aufgerufen werden kann


#funktionen aufrufen

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#ENDLOS-SCHLEIFE
i = 1
while i == 1:
    feuchtigkeitswert = sensor.read_u16()
    print(feuchtigkeitswert)
    anfangswert = int(feuchtigkeitswert)
    giessen(feuchtigkeitswert, anfangswert)
