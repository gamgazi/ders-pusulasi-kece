"""Alpha-only cleanup of the visually inspected ring/little-finger paper web."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent.parent
src=root/'adaylar/protez_el_001/r03/protez_el_001_r03.png'
dst=root/'teknik-islem/protez_el_001_alfa_bosluk.png'
assert not dst.exists(), 'Refusing overwrite'
a=np.array(Image.open(src).convert('RGBA')); before=a.copy()
path=[(1035,250),(1030,265),(1026,280),(1025,300),(1022,320),(1018,340),(1020,360),(1018,380),(1013,400),(1012,420),(1007,440),(1005,460),(1006,474)]
mask=Image.new('L',(a.shape[1],a.shape[0]),0); ImageDraw.Draw(mask).line(path,fill=255,width=7)
hole=np.array(mask)>0
changed=hole&(a[:,:,3]>0)
assert 500<int(changed.sum())<2000
# The reviewed channel must stay entirely within pale paper/gray crease, never colored ink.
visible=a[:,:,:3][changed&(a[:,:,3]>=16)].astype(int)
assert visible.min()>60 and (visible.max(1)-visible.min(1)).max()<50, 'Mask intersects colored ink; stop'
a[hole,3]=0
assert np.array_equal(a[:,:,:3],before[:,:,:3])
assert np.array_equal(a[~hole],before[~hole])
Image.fromarray(a,'RGBA').save(dst)
proof={'authorization':'Yerel teknik düzeltmeyi uygula','operation':'alpha-only narrow channel through inspected pale paper web between ring and little finger; preserve colored drawing and white inner margins','source':str(src.relative_to(root)),'target':str(dst.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'mask_polyline_native_pixels':path,'mask_width_pixels':7,'changed_alpha_pixels':int(changed.sum()),'all_rgb_pixels_unchanged':True,'pixels_outside_mask_unchanged':True,'upscaled':False,'visual_review_required':True}
(root/'denetim/protez_el_alfa_bosluk_kaniti.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(proof,ensure_ascii=False))
