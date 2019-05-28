
extension = ".png";

dir1 = "C:\\Users\\marek\\Desktop\\newSet\\";

setBatchMode(true);
n = 0;
processFolder(dir1);

function processFolder(dir1) {
	list = getFileList(dir1);
	for (i=0; i<list.length; i++) {
		if (endsWith(list[i], "/"))
			processFolder(dir1+list[i]);
		else if (endsWith(list[i], extension))
			processImage(dir1, list[i]);
	}
}

function processImage(dir1, name) {
	open(dir1+name);
	//run("Size...", "width=28 height=28 constrain average interpolation=None");
	//run("Find Edges");
	
	run("Compile and Run...", "compile=C:/Users/marek/Downloads/ij152-win-java8/ImageJ/plugins/Examples/Convert.java");
	selectWindow("NewImage");
	
	saveAs(extension, dir1+name);
	close();
}