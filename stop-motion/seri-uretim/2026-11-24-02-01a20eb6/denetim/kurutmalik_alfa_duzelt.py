from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/kurutmalik_camasir_bos_001/r01/kurutmalik_camasir_bos_001_r01.png'
dst=root/'teknik-islem/kurutmalik_camasir_bos_001_alfa_bosluk.png'
assert not dst.exists()
a=np.array(Image.open(src).convert('RGBA'));before=a.copy()
white=(a[:,:,:3].min(2)>180)&(a[:,:,3]>220)
labels,n=ndimage.label(white)
regions=[]
for lid in range(1,n+1):
 r=labels==lid;size=int(r.sum())
 if size<80:continue
 y,x=np.where(r);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
 if box[0]>250 and box[2]<1380 and box[1]>130 and box[3]<600:regions.append({'label':lid,'size':size,'bbox':box,'seed':[int(x[0]),int(y[0])]})
print(json.dumps(regions))
expected={52:412,74:1325,95:2199,116:1149}
inside=np.zeros(a.shape[:2],bool);details=[]
for lid,sz in expected.items():
 r=labels==lid;assert int(r.sum())==sz
 cut=ndimage.binary_erosion(r,structure=np.ones((3,3)),iterations=3)
 assert int(cut.sum())>40
 inside|=cut
 details.append({'label':lid,'white_region_pixels':sz,'alpha_changed':int(cut.sum())})
a[inside,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~inside],before[~inside])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only cleanup of four small white plugs inside rack frame, preserving 3px white scissor margins','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'regions':details,'changed_alpha_pixels':int(inside.sum()),'all_rgb_pixels_unchanged':True,'pixels_outside_holes_unchanged':True,'upscaled':False,'visual_review_required':True}
(root/'denetim/kurutmalik_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
