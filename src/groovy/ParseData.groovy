package groovy

class ParseData {

	
	public static final String abortion = new File("").absolutePath + '/data/abortion/';
	public static final String authors = new File("").absolutePath + '/data/authors/';
	public static final String gayRights = new File("").absolutePath + '/data/gayRights/';
	public static final String marijuana = new File("").absolutePath + '/data/marijuana/';
	public static final String obama =  new File("").absolutePath + '/data/obama/';
	
	
	def readFile(path)
	{
		def dataStructs = []
		
		DataStruct dataStruct = new DataStruct();
		dataStruct.sentence = new File(path).text
		
		dataStructs.add(dataStruct);
	}
	
	
	
}



