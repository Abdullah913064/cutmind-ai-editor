import argparse, math, os, re, subprocess
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf

W,H,FPS = 1280,720,18
SR=24000

MODULES=[
 dict(title='Algebra Is a Tool, Not a Monster', concept='Algebra describes unknown quantities and relationships.', intuition='Think of a sealed box. You can see what goes in and what comes out before you know what is inside.', rule='A letter such as x is simply a placeholder for a number.', example='Three boxes cost 150 rupees. If each box has the same price, 3x = 150.', steps=['3x = 150','x = 150 ÷ 3','x = 50'], test='If one ticket costs x rupees, five tickets cost 5x.', mistake='Treating x as a mysterious symbol instead of a number you do not know yet.', practice='A cricket bat costs x rupees. Two bats and a 200 rupee grip cost 2200 rupees. Write the equation.', answer='2x + 200 = 2200', visual='box'),
 dict(title='Variables, Constants and Coefficients', concept='Expressions contain pieces with different jobs: variables can change, constants stay fixed, and coefficients multiply variables.', intuition='Imagine a jersey order. Player count can change, setup cost can stay fixed, and price per jersey multiplies the player count.', rule='In 350x + 500, x is the variable, 350 is the coefficient, and 500 is the constant.', example='For x jerseys at 350 rupees each plus 500 rupees setup, total cost is 350x + 500.', steps=['variable → x','coefficient → 350','constant → 500'], test='7y - 12 has variable y, coefficient 7, and constant negative 12.', mistake='Calling every number a coefficient. A number without a variable is a constant.', practice='In 40x + 15y + 100, identify the variables, coefficients, and constant.', answer='variables: x, y • coefficients: 40, 15 • constant: 100', visual='jersey'),
 dict(title='Build Expressions from Real Situations', concept='Expressions are compact descriptions of calculations. They do not need an equals sign.', intuition='A bill is a story converted into arithmetic. Algebra lets one bill formula work for many quantities.', rule='Translate one phrase at a time. Per item usually means multiplication, and plus fee means addition.', example='A taxi charges 60 rupees base fare plus 14 rupees per kilometre. For k kilometres, cost is 60 + 14k.', steps=['base fare → 60','per km → 14k','combine → 60 + 14k'], test='Three notebooks at p rupees each and a 20 rupee pen give 3p + 20.', mistake='Putting an equals sign into an expression before there is a total value to equal.', practice='A shop sells x T-shirts at 399 rupees each and charges 80 rupees delivery. Write the expression.', answer='399x + 80', visual='bill'),
 dict(title='Like Terms and Simplifying', concept='Like terms have the same variable part and can be combined.', intuition='You can combine three apples and five apples, but you cannot call three apples plus five oranges eight apples.', rule='Add or subtract coefficients only when the variable part matches exactly.', example='3x + 5x = 8x because both terms represent the same kind of x quantity.', steps=['same variable → x','add coefficients → 3 + 5','result → 8x'], test='4x + 2y + 3x - y simplifies to 7x + y.', mistake='Combining 2x and 2x squared. They are not like terms.', practice='Simplify 6a + 4b - 2a + 3b.', answer='4a + 7b', visual='fruit'),
 dict(title='Equations Are Balances', concept='An equation says two quantities are equal. Solving means finding the value that keeps both sides balanced.', intuition='Picture a weighing scale. Whatever operation you do on one side, do the same on the other.', rule='Use inverse operations to isolate the variable while preserving equality.', example='x + 7 = 19. Subtract 7 from both sides.', steps=['x + 7 = 19','x + 7 - 7 = 19 - 7','x = 12'], test='5x = 45, so x = 9.', mistake='Changing only one side of an equation. Equality must be preserved.', practice='Solve 3x + 4 = 25.', answer='x = 7', visual='scale'),
 dict(title='Brackets and the Distributive Property', concept='A number outside brackets multiplies every term inside the brackets.', intuition='If three teams each receive two balls and one cone, then every team receives both items.', rule='a times open bracket b plus c close bracket equals ab plus ac.', example='3(x + 4) = 3x + 12.', steps=['3 × x = 3x','3 × 4 = 12','result → 3x + 12'], test='2(5y - 3) = 10y - 6.', mistake='Multiplying only the first term inside the brackets.', practice='Expand 4(2x + 5).', answer='8x + 20', visual='teams'),
 dict(title='Fractions, Ratios and Proportion', concept='Fractions in algebra behave like ordinary fractions; the variable simply stands for a number.', intuition='A team budget split equally among players is division, even if we do not yet know the exact budget.', rule='To remove a denominator, multiply both sides by that denominator.', example='x divided by 4 equals 6, so x equals 24.', steps=['x ÷ 4 = 6','multiply both sides by 4','x = 24'], test='If three shirts cost 900 rupees, one shirt costs 900 divided by 3, which is 300 rupees.', mistake='Multiplying or dividing only part of one side of the equation.', practice='Solve x divided by 5 plus 2 equals 8.', answer='x = 30', visual='fraction'),
 dict(title='Turn Word Problems into Equations', concept='Word problems become easier when you separate known values, unknown values, and the relationship between them.', intuition='You are translating from everyday language into mathematical language.', rule='Choose the unknown first, then build the equation sentence by sentence.', example='After spending 250 rupees, Ali has 750 rupees left. If x was his starting money, x - 250 = 750.', steps=['unknown start money → x','spent 250 → x - 250','left 750 → x - 250 = 750'], test='A number doubled and increased by 9 gives 31, so 2x + 9 = 31.', mistake='Trying to calculate before defining what the unknown represents.', practice='Three equal match fees plus 500 rupees travel cost total 3500 rupees. Find each match fee.', answer='3x + 500 = 3500 → x = 1000', visual='translate'),
 dict(title='Coordinates and Linear Relationships', concept='A linear relationship connects two variables at a constant rate and can be drawn as a straight line.', intuition='If each extra jersey always adds the same cost, total cost rises at a constant rate.', rule='In y = mx + b, m is the rate of change and b is the starting value.', example='y = 350x + 500 means 350 rupees per jersey and 500 rupees starting cost.', steps=['b = 500 → starting cost','m = 350 → cost per jersey','x → quantity, y → total'], test='For y = 2x + 1, when x = 3, y = 7.', mistake='Confusing the starting value with the rate of change.', practice='For y = 40x + 100, what is y when x = 5?', answer='y = 300', visual='graph'),
 dict(title='Final Challenge: Think Algebraically', concept='Real algebra is recognizing structure, representing it, solving it, and checking whether the answer makes sense.', intuition='Like solving a cricket field problem: observe the situation, choose the right tool, execute, then verify.', rule='Represent, simplify, solve, then check.', example='A shop has a 150 rupee fixed delivery charge and 275 rupees per item. Total is 1800 rupees.', steps=['275x = 1650','x = 6','check → 275×6 + 150 = 1800'], test='2(x + 5) = 26 becomes 2x + 10 = 26, so x = 8.', mistake='Stopping as soon as you get a number without checking it in the original relationship.', practice='Solve and check: 4(x - 2) + 3 = 27.', answer='4x - 8 + 3 = 27 → 4x = 32 → x = 8', visual='cricket'),
]

INTRO_TMPL='''We are starting {num}. {title}. {concept} For the next few minutes, do not try to memorize symbols or copy steps. First understand what the situation means. Then convert that meaning into algebra. Ask three questions: what do I know, what do I not know, and how are those quantities connected? If you can answer those questions, beginner algebra becomes much less scary. The goal is not speed. The goal is to build a mental picture strong enough that the symbols feel natural. By the end of this module, you should be able to explain the idea in ordinary language before writing an equation.'''
INTUITION_TMPL='''Here is the intuition. {intuition} {concept} Notice that the mathematics exists before we write a single symbol. Symbols only compress the idea. Imagine the situation clearly and say it in your own words. What is changing? What stays fixed? What is being multiplied, added, divided, or compared? When learners get stuck, they often stare at x or y. Instead, look behind the letter and ask what real quantity it represents. Once that is clear, algebra becomes a short language for a relationship you already understand. Keep this habit for the entire course.'''
RULE_TMPL='''Now we can state the rule. {rule} A rule is useful only when you understand why it works, so connect it to this example. {example} Read the expression slowly as a sentence. Point to each piece and explain its job. Ask whether the number is a starting amount, a repeated amount, a rate, or a fixed value. Do not rush to calculate. In algebra, representation comes before calculation. If the representation is wrong, perfect arithmetic will still give the wrong answer. If the representation is right, the arithmetic is usually the easy part. Use the rule as a description of structure, not as a magic formula.'''
STEPS_TMPL='''Watch the steps carefully. We start with {s1}. Then {s2}. Finally {s3}. Do not just watch the symbols move. Ask what operation happened and why it was allowed. A strong learner can pause after any line and explain the transition in plain language. That explanation is more valuable than memorizing a shortcut. Now mentally reverse the steps and check whether the result returns to the original situation. This backward check catches sign errors, missed terms, and careless arithmetic. When you solve your own problems, use the same rhythm: one small step, one reason, then a quick check.'''
TEST_TMPL='''Let us test the idea with another example. {test} The numbers look different, but the structure is the same. That matters because algebra is about patterns that survive when the numbers change. Now notice a common error: {mistake} Instead of memorizing a warning, understand why the mistake is wrong. Ask what quantity each term represents and whether the proposed operation preserves that meaning. When you feel unsure, return to the real situation or substitute a simple number and test it. Meaning and checking are your two fastest error-detection tools. Comparing a correct pattern with a tempting wrong pattern builds mathematical judgment.'''
PRACTICE_TMPL='''Your turn. {practice} Do not look at the answer immediately. First say what the unknown represents. Then write one line that connects the known information to that unknown. Pause the video and give yourself about twenty seconds. Now compare your work with this: {answer}. If your answer was different, do not simply replace it. Find the exact line where your reasoning changed. Was the variable defined differently? Did you choose the wrong operation? Did arithmetic cause the error? Fix that exact point and solve again. That correction is where learning happens. Finally, explain the answer aloud in one sentence so it connects back to the original situation.'''

def make_scenes(midx):
    m=MODULES[midx]
    return [INTRO_TMPL.format(num=midx+1, **m), INTUITION_TMPL.format(**m), RULE_TMPL.format(**m), STEPS_TMPL.format(s1=m['steps'][0],s2=m['steps'][1],s3=m['steps'][2]), TEST_TMPL.format(**m), PRACTICE_TMPL.format(**m)]

def split_sentences(text): return [p.strip() for p in re.split(r'(?<=[.!?])\s+',text.strip()) if p.strip()]

def load_font(size,bold=False):
    paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
    for p in paths:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def wrap_text(draw,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        cand=(cur+' '+w).strip()
        if draw.textbbox((0,0),cand,font=font)[2] <= maxw: cur=cand
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def text_layer(text,box_w,box_h,size=40,bold=False,color=(245,248,255,255)):
    im=Image.new('RGBA',(box_w,box_h),(0,0,0,0)); d=ImageDraw.Draw(im); f=load_font(size,bold); lines=wrap_text(d,text,f,box_w-40); line_h=int(size*1.25); y=max(0,(box_h-line_h*len(lines))//2)
    for line in lines:
        bb=d.textbbox((0,0),line,font=f); x=(box_w-(bb[2]-bb[0]))//2; d.text((x,y),line,font=f,fill=color); y+=line_h
    return np.array(im)

def alpha_blend(frame,layer,x,y,alpha=1.0):
    h,w=layer.shape[:2]; x=int(x); y=int(y); x0=max(0,x); y0=max(0,y); x1=min(W,x+w); y1=min(H,y+h)
    if x1<=x0 or y1<=y0:return
    lx0=x0-x; ly0=y0-y; lx1=lx0+(x1-x0); ly1=ly0+(y1-y0); src=layer[ly0:ly1,lx0:lx1,:3][:,:,::-1].astype(np.float32); a=(layer[ly0:ly1,lx0:lx1,3:4].astype(np.float32)/255)*alpha; dst=frame[y0:y1,x0:x1].astype(np.float32); frame[y0:y1,x0:x1]=(src*a+dst*(1-a)).astype(np.uint8)

def base_frame(t):
    yy=np.linspace(0,1,H)[:,None,None]; c1=np.array([35,20,9],float); c2=np.array([21,11,5],float); arr=np.tile(c1*(1-yy)+c2*yy,(1,W,1)); X,Y=np.meshgrid(np.arange(W),np.arange(H)); dist=((X-W*.55)/(W*.75))**2+((Y-H*.45)/(H*.7))**2; arr+=np.clip(1-dist,0,1)[...,None]*np.array([20,12,2]); frame=np.clip(arr,0,255).astype(np.uint8)
    for x in range(0,W,64): cv2.line(frame,(x,0),(x,H),(26,35,49),1)
    for y in range(0,H,64): cv2.line(frame,(0,y),(W,y),(26,35,49),1)
    for i in range(20): cv2.circle(frame,(int((i*83+t*18*(1+i%3))%W),int((i*47+math.sin(t*.4+i)*30+i*19)%H)),1+(i%2),(55,74,90),-1)
    return frame

def rounded_rect(img,p1,p2,color,rad=24):
    x1,y1=p1;x2,y2=p2;cv2.rectangle(img,(x1+rad,y1),(x2-rad,y2),color,-1);cv2.rectangle(img,(x1,y1+rad),(x2,y2-rad),color,-1)
    for cx,cy in [(x1+rad,y1+rad),(x2-rad,y1+rad),(x1+rad,y2-rad),(x2-rad,y2-rad)]:cv2.circle(img,(cx,cy),rad,color,-1)

def draw_box(frame,cx,cy,s=1,label='?'):
    w=int(180*s);h=int(145*s);d=int(35*s);p=np.array([[cx-w//2,cy-h//2],[cx+w//2,cy-h//2],[cx+w//2,cy+h//2],[cx-w//2,cy+h//2]],np.int32);cv2.polylines(frame,[p],True,(90,190,255),6);cv2.line(frame,tuple(p[0]),(p[0][0]+d,p[0][1]-d),(90,190,255),4);cv2.line(frame,tuple(p[1]),(p[1][0]+d,p[1][1]-d),(90,190,255),4);cv2.line(frame,(p[0][0]+d,p[0][1]-d),(p[1][0]+d,p[1][1]-d),(90,190,255),4);cv2.putText(frame,label,(cx-int(32*s),cy+int(25*s)),cv2.FONT_HERSHEY_SIMPLEX,2*s,(90,190,255),5,cv2.LINE_AA)

def draw_jersey(frame,cx,cy,s=1,label='x'):
    pts=np.array([[cx-55*s,cy-70*s],[cx-100*s,cy-35*s],[cx-75*s,cy+5*s],[cx-55*s,cy-8*s],[cx-55*s,cy+90*s],[cx+55*s,cy+90*s],[cx+55*s,cy-8*s],[cx+75*s,cy+5*s],[cx+100*s,cy-35*s],[cx+55*s,cy-70*s],[cx+30*s,cy-50*s],[cx-30*s,cy-50*s]],dtype=np.int32);cv2.fillPoly(frame,[pts],(70,140,210));cv2.polylines(frame,[pts],True,(120,220,255),3);cv2.putText(frame,label,(int(cx-18*s),int(cy+25*s)),cv2.FONT_HERSHEY_SIMPLEX,1.2*s,(245,245,245),3,cv2.LINE_AA)

def draw_fruit(frame,cx,cy,s=1,orange=False):
    col=(0,150,255) if orange else (70,70,235);cv2.circle(frame,(int(cx),int(cy)),int(36*s),col,-1);cv2.ellipse(frame,(int(cx+10*s),int(cy-36*s)),(int(17*s),int(8*s)),-30,0,360,(70,180,100),-1)

def draw_scale(frame,cx,cy,s=1,tilt=0):
    cv2.line(frame,(cx,cy-95),(cx,cy+100),(160,190,210),8);cv2.line(frame,(cx-70,cy+105),(cx+70,cy+105),(160,190,210),8);dy=int(tilt*30);cv2.line(frame,(cx-190,cy-65+dy),(cx+190,cy-65-dy),(90,220,255),7)
    for x,yy in [(cx-150,cy-65+dy),(cx+150,cy-65-dy)]:cv2.line(frame,(x,yy),(x-45,yy+90),(180,200,220),3);cv2.line(frame,(x,yy),(x+45,yy+90),(180,200,220),3);cv2.ellipse(frame,(x,yy+100),(70,18),0,0,180,(120,180,220),4)

def draw_fraction(frame,cx,cy,s=1):
    cv2.circle(frame,(cx,cy),int(100*s),(90,180,240),4);cv2.line(frame,(cx,cy),(cx,cy-int(100*s)),(90,180,240),4);cv2.line(frame,(cx,cy),(cx+int(100*s),cy),(90,180,240),4);cv2.ellipse(frame,(cx,cy),(int(95*s),int(95*s)),-90,0,90,(90,190,255),-1)

def draw_graph(frame,cx,cy,s=1):
    w,h=int(360*s),int(260*s);x0=cx-w//2;y0=cy+h//2;cv2.line(frame,(x0,y0),(x0+w,y0),(170,190,210),3);cv2.line(frame,(x0,y0),(x0,y0-h),(170,190,210),3);cv2.line(frame,(x0+20,y0-20),(x0+w-25,y0-h+35),(90,220,255),6)
    for i in range(1,5):cv2.circle(frame,(x0+int(i*w/5),y0-int(i*h/5)),7,(120,245,150),-1)

def draw_teams(frame,cx,cy,s=1):
    for i,dx in enumerate([-220,0,220]):
        x=int(cx+dx*s);cv2.circle(frame,(x,int(cy-55*s)),int(30*s),(90,180,245),-1);cv2.rectangle(frame,(x-int(30*s),int(cy-15*s)),(x+int(30*s),int(cy+70*s)),(60,120,210),-1);cv2.circle(frame,(x-int(55*s),int(cy+100*s)),int(18*s),(60,220,255),-1);pts=np.array([[x+35*s,cy+122*s],[x+65*s,cy+70*s],[x+95*s,cy+122*s]],np.int32);cv2.polylines(frame,[pts],True,(90,190,255),5)

def draw_translate(frame,cx,cy,s=1):
    rounded_rect(frame,(cx-360,cy-105),(cx-70,cy+105),(35,60,90),22);rounded_rect(frame,(cx+70,cy-105),(cx+360,cy+105),(35,60,90),22);cv2.arrowedLine(frame,(cx-40,cy),(cx+40,cy),(90,220,255),7,tipLength=.25);cv2.putText(frame,'WORDS',(cx-310,cy+10),cv2.FONT_HERSHEY_SIMPLEX,1.05,(245,245,245),3,cv2.LINE_AA);cv2.putText(frame,'EQUATION',(cx+105,cy+10),cv2.FONT_HERSHEY_SIMPLEX,.9,(120,245,150),3,cv2.LINE_AA)

def draw_cricket(frame,cx,cy,s=1):
    cv2.ellipse(frame,(cx,cy),(int(330*s),int(190*s)),0,0,360,(70,140,70),-1);cv2.ellipse(frame,(cx,cy),(int(330*s),int(190*s)),0,0,360,(110,190,110),4);cv2.rectangle(frame,(cx-int(25*s),cy-int(140*s)),(cx+int(25*s),cy+int(140*s)),(150,190,210),-1);cv2.circle(frame,(cx-int(130*s),cy+int(20*s)),int(14*s),(80,80,235),-1)

def draw_bill(frame,cx,cy,s=1):
    x1,y1=int(cx-170*s),int(cy-180*s);x2,y2=int(cx+170*s),int(cy+180*s);rounded_rect(frame,(x1,y1),(x2,y2),(235,235,235),18)
    for i,w in enumerate([220,180,240,150]):cv2.line(frame,(x1+35,y1+60+i*55),(x1+35+w,y1+60+i*55),(80,90,100),3)
    cv2.putText(frame,'TOTAL',(x1+35,y2-45),cv2.FONT_HERSHEY_SIMPLEX,.7,(20,35,55),2,cv2.LINE_AA)

def draw_visual(frame,visual,kind,phase):
    bob=math.sin(phase*math.pi*2)*5
    if kind==0:
        for i,(txt,x,y) in enumerate([('x',350,330),('=',520,300),('?',690,350),('+',860,290)]):cv2.putText(frame,txt,(x,int(y+bob*(i%2*2-1))),cv2.FONT_HERSHEY_SIMPLEX,2.6,(90,220,255) if i%2==0 else (120,245,150),6,cv2.LINE_AA)
    elif kind==1:
        if visual=='box':draw_box(frame,640,int(355+bob),1.3)
        elif visual=='jersey':
            for i,x in enumerate([470,640,810]):draw_jersey(frame,x,int(355+bob*(i-1)),.8,str(i+1))
        elif visual=='bill':draw_bill(frame,640,int(360+bob),.9)
        elif visual=='fruit':
            for i,x in enumerate([430,510,590]):draw_fruit(frame,x,355+i%2*5,.85,False)
            for i,x in enumerate([720,800,880]):draw_fruit(frame,x,355+i%2*5,.85,True)
        elif visual=='scale':draw_scale(frame,640,int(370+bob),1,.15*math.sin(phase*6.28))
        elif visual=='teams':draw_teams(frame,640,int(340+bob),.85)
        elif visual=='fraction':draw_fraction(frame,640,int(365+bob),1.15)
        elif visual=='translate':draw_translate(frame,640,int(360+bob),1)
        elif visual=='graph':draw_graph(frame,640,int(390+bob),1.15)
        elif visual=='cricket':draw_cricket(frame,640,int(365+bob),1)
    elif kind==2:
        rounded_rect(frame,(250,240),(1030,500),(25,45,70),30);cv2.rectangle(frame,(250,240),(1030,500),(80,180,220),3)
    elif kind==3:
        xs=[350,640,930]
        for i,x in enumerate(xs):
            col=(50,125,190) if phase<i/3 else (70,180,220);cv2.circle(frame,(x,365),72,col,-1);cv2.circle(frame,(x,365),72,(120,220,255),3)
            if i<2:cv2.arrowedLine(frame,(x+80,365),(xs[i+1]-80,365),(120,170,200),4,tipLength=.2)
    elif kind==4:
        rounded_rect(frame,(170,245),(600,500),(30,70,55),26);rounded_rect(frame,(680,245),(1110,500),(65,35,50),26);cv2.putText(frame,'WORKS',(300,310),cv2.FONT_HERSHEY_SIMPLEX,.9,(120,245,150),3,cv2.LINE_AA);cv2.putText(frame,'TRAP',(830,310),cv2.FONT_HERSHEY_SIMPLEX,.9,(120,120,255),3,cv2.LINE_AA);cv2.putText(frame,'OK',(315,430),cv2.FONT_HERSHEY_SIMPLEX,1.6,(120,245,150),5,cv2.LINE_AA);cv2.putText(frame,'X',(850,430),cv2.FONT_HERSHEY_SIMPLEX,2.2,(120,120,255),5,cv2.LINE_AA)
    else:
        cv2.circle(frame,(640,340),120,(50,70,90),18);cv2.ellipse(frame,(640,340),(120,120),-90,0,int(360*phase),(90,220,255),18);cv2.putText(frame,'TRY',(575,355),cv2.FONT_HERSHEY_SIMPLEX,1.2,(245,245,245),4,cv2.LINE_AA)

def key_text(m,kind):
    return [m['concept'],m['intuition'],m['rule']+'  '+m['example'],'   →   '.join(m['steps']),m['test']+'  Common trap: '+m['mistake'],m['practice']+'  '+m['answer']][kind]

def generate_scene_audio(pipeline,text,outwav,practice=False):
    sentences=split_sentences(text);parts=[];timeline=[];cursor=0.0
    for s in sentences:
        if practice and s.startswith('Now compare'):
            silence=np.zeros(int(SR*20),dtype=np.float32);parts.append(silence);cursor+=20
        chunks=[]
        for result in pipeline(s,voice='af_heart',speed=1.03):
            audio=result.output if hasattr(result,'output') else result[2]
            if audio is not None:chunks.append(np.asarray(audio,dtype=np.float32))
        if not chunks:continue
        audio=np.concatenate(chunks);timeline.append((cursor,cursor+len(audio)/SR,s));parts.append(audio);parts.append(np.zeros(int(SR*.16),dtype=np.float32));cursor+=len(audio)/SR+.16
    full=np.concatenate(parts) if parts else np.zeros(SR,dtype=np.float32);peak=max(.01,float(np.max(np.abs(full))));full=(full/peak*.92).astype(np.float32);sf.write(outwav,full,SR);return len(full)/SR,timeline

def render_scene(midx,kind,audio_path,duration,timeline,outmp4):
    m=MODULES[midx];cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(audio_path),'-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest',str(outmp4)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);title=text_layer(f'{midx+1}. {m["title"]}',1040,100,44,True);key=text_layer(key_text(m,kind),1000,150,34);caps=[(st,en,text_layer(s,1040,112,28)) for st,en,s in timeline];frames=max(1,int(math.ceil(duration*FPS)))
    for fi in range(frames):
        t=fi/FPS;frame=base_frame(t);cv2.putText(frame,'ALGEBRA • ZERO TO CONFIDENCE',(60,58),cv2.FONT_HERSHEY_SIMPLEX,.55,(130,155,180),2,cv2.LINE_AA);cv2.putText(frame,f'CHAPTER {midx+1}/10  •  SCENE {kind+1}/6',(890,58),cv2.FONT_HERSHEY_SIMPLEX,.5,(130,155,180),1,cv2.LINE_AA);alpha_blend(frame,title,120,82);draw_visual(frame,m['visual'],kind,t/max(.1,duration));alpha_blend(frame,key,140,500,.96)
        for st,en,cap in caps:
            if st<=t<en:alpha_blend(frame,cap,120,600,.92);break
        cv2.rectangle(frame,(0,H-7),(int(W*min(1,t/max(.1,duration))),H),(90,220,255),-1);proc.stdin.write(frame.tobytes())
    proc.stdin.close();code=proc.wait()
    if code:raise RuntimeError(f'ffmpeg failed {code}')

def concat_mp4(files,out):
    listfile=Path(out).with_suffix('.txt');listfile.write_text('\n'.join("file '"+str(Path(f).resolve()).replace("'","'\\''")+"'" for f in files));subprocess.check_call(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(listfile),'-c','copy',str(out)])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--chapter',type=int,required=True);ap.add_argument('--outdir',default='output');args=ap.parse_args();midx=args.chapter-1;outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    from kokoro import KPipeline
    pipeline=KPipeline(lang_code='a');rendered=[]
    for kind,text in enumerate(make_scenes(midx)):
        wav=outdir/f'c{args.chapter:02d}_s{kind+1:02d}.wav';mp4=outdir/f'c{args.chapter:02d}_s{kind+1:02d}.mp4';dur,timeline=generate_scene_audio(pipeline,text,wav,practice=(kind==5));print(f'chapter {args.chapter} scene {kind+1}: {dur:.1f}s');render_scene(midx,kind,wav,dur,timeline,mp4);rendered.append(mp4)
    chapter=outdir/f'chapter_{args.chapter:02d}.mp4';concat_mp4(rendered,chapter);print(chapter)

if __name__=='__main__':main()
