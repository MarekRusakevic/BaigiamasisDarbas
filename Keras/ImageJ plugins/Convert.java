

import ij.*;
import ij.plugin.filter.PlugInFilter;
import ij.process.*;
import java.awt.*;
import ij.io.FileSaver;



public class Convert implements PlugInFilter {

	ImagePlus imp;

	public int setup(String arg, ImagePlus imp) {
		this.imp = imp;
		return DOES_ALL;
	}

	public void run(ImageProcessor ip) {
		
		boolean fIsStack = false;
		ImageStack stackOld = imp.getStack();
		
		if ((stackOld != null) && (stackOld.getSize() > 1))
			fIsStack = true;
		
	
		if (fIsStack) {
			ImageStack stackNew = expandStack(stackOld, 100, 100);
			new ImagePlus("NewStack", stackNew).show();
		} else {
			ImageProcessor newIP = expandImage(ip, 100, 100);
			new ImagePlus("NewImage", newIP).show();
		}
	
	}
	
	
	public ImageStack expandStack(ImageStack stackOld, int widthNew, int heightNew) {
		int nFrames = stackOld.getSize();
		
		ImageStack stackNew = new ImageStack(widthNew, heightNew);

		for (int i=1; i<=nFrames; i++) {
			
			ImageProcessor ipOld = stackOld.getProcessor(i);
			
			ImageProcessor ipNew = convert(ipOld);
			
			ipNew = ipNew.resize(widthNew,heightNew);
			
			stackNew.addSlice(null, ipNew);
		}
		return stackNew;
	}
	
	
	public ImageProcessor expandImage(ImageProcessor ipOld, int widthNew, int heightNew) {
		ImageProcessor ipNew = convert(ipOld);
		ipNew = ipNew.resize(widthNew,heightNew);
		return ipNew;
	}
	
	
	public ImageProcessor convert(ImageProcessor ip){
		
		int widthStart = -1;
		int widthEnd = -1;
		
		int heightStart = -1;
		int heightEnd = -1;

		Rectangle r = ip.getRoi();

		for (int y=r.y; y<(r.y+r.height); y++){
			for (int x=r.x; x<(r.x+r.width); x++){
				
				if(ip.get(x,y) > 20){
					
					if(heightStart == -1){
						heightStart = y;
					}
					break;
					
				} else if(x == r.x+r.width - 1){
					
					if(heightStart != -1){
					
						if(heightEnd == -1){
							heightEnd = y;
							break;
						}
						
					}

				}
			}
		}
		
		for (int x=r.x; x<(r.x+r.width); x++){
			for (int y=r.y; y<(r.y+r.height); y++){
				
				if(ip.get(x,y) > 20){
					
					if(widthStart == -1){
						widthStart = x;
					}
					break;
					
				} else if(y == r.y+r.height - 1){
					
					if(widthStart != -1){
					
						if(widthEnd == -1){
							widthEnd = x;
							break;
						}
						
					}

				}
				
			}
		}


		if(widthStart == -1){
			widthStart = 0;
		} 
		if(widthEnd == -1){
			widthEnd = ip.getWidth();
		} 
		if(heightStart == -1){
			heightStart = 0;
		}
		if(heightEnd == -1){
			heightEnd = ip.getHeight();
		}
		
		
		int width = widthEnd - widthStart;
		int height = heightEnd - heightStart;
		
		ImageProcessor ip2 = ip.resize(width,height);

		Rectangle r2 = ip2.getRoi();
		for (int y=r2.y; y<(r2.y+r2.height); y++){
			for (int x=r2.x; x<(r2.x+r2.width); x++){
				
				ip2.set(x, y, ip.get(x + widthStart, y + heightStart));

			}
		}
	
		return ip2;
	
	}

}