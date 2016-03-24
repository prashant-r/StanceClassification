
class HelloWorld {

	static void main(String [] args) {
		//Creating an empty list
		def technologies = []
		
		// As with Java
		technologies.add("Grails")
		
		// Left shift adds, and returns the list
		technologies << "Groovy"
		
		// Add multiple elements
		technologies.addAll(["Gradle","Griffon", "Gradle"])
		
		technologies = technologies - "Gradle"
		
		println technologies;
	}
}
