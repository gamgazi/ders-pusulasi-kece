from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/paten_buz_tek_001/r01/paten_buz_tek_001_r01.png'
dst=root/'teknik-islem/paten_buz_tek_001_alfa_bosluk.png'
assert not dst.exists()
a=np.array(Image.open(src).convert('RGBA'));before=a.copy()
roi=np.zeros(a.shape[:2],bool);roi[735:835,530:1030]=True
white=(a[:,:,:3].min(2)>200)&(a[:,:,3]>220)&roi
labels,n=ndimage.label(white);label=int(labels[780,800]);assert label>0
region=labels==label;y,x=np.where(region)
print(json.dumps({'region':int(region.sum()),'bbox':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]}))
assert int(region.sum())==29428
assert [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]==[554,749,1017,823]
inside=ndimage.binary_erosion(region,structure=np.ones((3,3)),iterations=8)
assert 18000<int(inside.sum())<24000
a[inside,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~inside],before[~inside])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only cleanup of central white blade/sole gap, retaining 8px white inner scissor margin','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'seed':[800,780],'white_region_pixels':29428,'changed_alpha_pixels':int(inside.sum()),'all_rgb_pixels_unchanged':True,'pixels_outside_holes_unchanged':True,'upscaled':False,'visual_review_required':True}
(root/'denetim/paten_buz_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
