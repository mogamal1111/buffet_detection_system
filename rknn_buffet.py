E=print
J=Exception
import json,time as N,logging as C,sys as A
from libraries.datasend import DataUploader as f
from libraries.utils import time_to_string as O,mat_to_response as g
from libraries.stream_publisher import StreamPublisher as h
from libraries.async_capture import VideoCaptureAsync as i
B=C.getLogger(__name__)
__version__='2.27'
__author__='TransformsAI'
def F(config):
	X='frame_count';W='last_heartbeat_time';V='streamer';U=None;T='heartbeat_url';S=False;M='last_inference_time';L='cap';K='X-Secret-Key';F=True;D='sn';C=config;Y=C.get('inference_interval',1.);Z=C.get('heartbeat_interval',60);j=C.get('frame_send_width',1920);k=C.get('frame_send_jpeg_quality',65);l=C.get('livestream',S);a=f(C['data_send_url'],C[T],{K:C[K]},project_version=__version__);P=[]
	for I in C.get('streams',[]):
		E=I.get(D)
		if not E:B.warning(f"Stream configuration missing 'sn'. Skipping this stream: {I}");continue
		Q=I.get('local_video_source')if I.get('local_video',F)else I.get('video_source')
		if not Q:B.warning(f"Stream {E}: Video source not specified. Skipping.");continue
		B.info(f"Initializing stream: {E} from source: {Q}");m={'enabled':F,D:E,'uploader_config':{'api_url':U,T:C.get(T),'headers':{K:C.get(K,'')},'debug':F,'max_workers':2,'source':'Video Capture','project_version':__version__}};b=i(src=Q,heartbeat_config=m,auto_restart_on_fail=F);b.start();R=U
		if l:
			try:R=h(f"live_{E}",start_stream=S,host=C.get('local_ip','127.0.0.1'),port=C.get('mqtt_port',1883));R.start_streaming();B.info(f"Livestream publisher started for stream {E} on topic live_{E}")
			except J as G:B.error(f"Failed to start livestreamer for stream {E}: {G}",exc_info=F)
		P.append({D:E,'config':I,L:b,V:R,M:N.time()-Y,W:N.time()-Z,X:0})
	if not P:B.error('No streams were successfully initialized. Exiting live detection.');return
	try:
		while F:
			for A in P:
				if not A[L]or not A[L].started:continue
				n,c=A[L].read()
				if not n:continue
				H=N.time();A[X]+=1
				if H-A[M]>=Y:
					B.debug(f"Stream {A[D]}: Triggering inference. Frame: {A[X]}");o={D:A[D],'is_ai_annotated':S,'start_time':O(A[M]),'end_time':O(H)};d=U;e=g(c,j,k,timestamp=H)
					if e:d={'image':e}
					else:B.warning(f"Stream {A[D]}: Image encoding failed.")
					try:a.send_data(o,files=d);B.info(f"Stream {A[D]}: Data sent.")
					except J as G:B.error(f"Stream {A[D]}: Error sending data: {G}",exc_info=F)
					if A[V]:A[V].updateFrame(c)
					A[M]=H
				if H-A[W]>=Z:
					try:p=a.send_heartbeat(A[D],timestamp=O(H));B.info(f"Stream {A[D]}: Heartbeat sent.");A[W]=H
					except J as G:B.error(f"Stream {A[D]}: Error sending heartbeat: {G}",exc_info=F)
	except J as G:B.error(f"Error in processing stream {A[D]}: {G}",exc_info=F)
if __name__=='__main__':
	C.basicConfig(level=C.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s');B.info('Starting Buffet Management System...')
	if len(A.argv)<2:E('Usage: python buffet.py <config_path>');A.exit(1)
	D=A.argv[1];E(f"Received config path: {D}")
	try:
		with open(D,'r')as G:H=json.load(G)
	except J as I:B.error(f"Failed to load configuration from {D}: {I}");A.exit(1)
	F(H)