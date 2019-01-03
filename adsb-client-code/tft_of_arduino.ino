#include <UTFT.h>
String tempStr;
String tempStrA;
String tempStrB;
char data;
int currentCol=0;
int count=0;
bool state=false;
extern uint8_t SmallFont[];
UTFT tft(QD220A,A2,A1,A5,A4,A3);

void printMessage(String inputStr)
{
   if(currentCol>150)
   { 
        delay(2000);
  tft.clrScr();
  currentCol=0; 
   }
  int currentX=0;
  
//  tft.print(tempStr,0,currentCol);
  String tempStr2="";
  String tempStr3="";
  for(int i=0;i<23;i++)
  {    
   tempStr2+=inputStr[i]; 
  }
  for(int i=23;i<inputStr.length();i++)
  {    
   tempStr3+=inputStr[i]; 
  }
  tft.print(tempStr2,0,currentCol);
  currentCol+=15;
  tft.print(tempStr3,0,currentCol);

  currentCol+=15;
  tempStr2="";
  tempStr3="";
  inputStr="";
  state=false; 
}

void setup() 
{
 tft.InitLCD();
 tft.setFont(SmallFont);
 tft.clrScr();
 tft.setColor(0,0,255);
 
 Serial.begin(19200);
}

void loop()
{
  Serial.print('A');
  while(Serial.available()==0);
  tft.clrScr();
  tempStrA="";
  while(Serial.available()!=0)
  {
    state=true;
    data=Serial.read();
    delay(2);
    tempStrA+=data;  
  }
  if(tempStrA[0]!='R')
  {
    if(tempStrA[1]==',')
    {
      count=tempStrA[0]-'0';
      tft.print("Num:",0,1);
      tft.print(tempStrA.substring(0,1),30,1);
      tft.print("Time:",0,15);
      tft.print(tempStrA.substring(2),6*6,15);
    }
    else if(tempStrA[2]==',')
    {
      count=tempStrA[0]-'0';
      count=count*10+(tempStrA[1]-'0');
      tft.print("Num:",0,1);
      tft.print(tempStrA.substring(0,2),30,1);
      tft.print("Time:",0,15);
      tft.print(tempStrA.substring(3),6*6,15);
    }
    else count=-1;
  }
  else
    return;

 currentCol=30;
 
 for(int t=0;t<count;t++)
 {
  Serial.print('B');
  while(Serial.available()==0);
  delay(200);
  tempStrB="";
  while(Serial.available()!=0)
  {
    state=true;
    data=Serial.read();
    delay(2);
    tempStrB+=data;  
  }
  if(tempStrB[0]=='R')
    return;

  printMessage(tempStrB);


 }
 delay(2000);
}

