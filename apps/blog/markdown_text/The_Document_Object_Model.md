
----------

# The Document Object Model (DOM)

The DOM is a cross-platform and language-independent document that treats an XML or HTML document as a tree structure where each node is an object representing a part of the document.

> 								HTML (root node)
> 								 |
> 					  Head -------------- Body (element node)
> 						|				    |
> 					  title         h1 --- div --- div
> 											|		
> 										p ----- p (element node)
> 										|
> 									text node

In JavaScript if you want to interact with the DOM document you need to reference it, like this:
								document.PROPERTY/METHOD

### Query Selector
The method querySelector goes trough the DOM and grabs the first element wanted and ignores the rest of them.
The method querySelectorAll instead of grabbing the first element grabs every element that matches the criteria. It returns a NodeList that can be acceded like a normal array.

 *Remember that the DOM is a **tree** of nodes!*

    document.querySelector*(query)

 !querySelector* refers to both, querySelector() and querySelectorAll()

Examples:

Grabbing the first p TAG:

	document.querySelector*('p')  <- Grabs the first p tag.

Grabbing the first element with the CLASS of error:

	document.querySelector*('.error')

Grabbing the first element with the ID of container:

	document.querySelector*('#container') <- Grabs the first element with the id of container.

You can grab specific elements by combining tag's, classes or id's, for example:

	document.querySelector*('h1#title_header.header_class')

This example grab's an h1 tag with an id of 'title_header' and a class of 'header_class'.

If you want to grab a tag inside another tag you need to do it like this:

	document.querySelector*('p > b')


### Get Element

There is another way to get elements in a DOM document and that is done with getElement*

	document.getElement*(query)

*Returns a HTMLCollection*

You can get several type of elements with this method:

	document.getElementById(query)
	
	document.getElementsByClassName(query)
	
	document.getElementsByTagName(query)

## Difference between getElementBy* and querySelector*

+ querySelector* is more flexible, as you can pass it any CSS3 selector, not just simple ones for id, tag, or class.

+ **The performance of querySelector* changes with the size of the DOM that it is invoked on.** To be precise, querySelector* calls run in O(n) time, n being the total number of all children of the element or document it is invoked on. getElement* calls run in O(1) time.

+ The return types of these calls vary. querySelector and getElementById both return a single element. querySelectorAll and getElementsByName both return NodeLists, being newer functions that were added after HTMLCollection went out of fashion. The older getElementsByClassName and getElementsByTagName both return HTMLCollections. Again, this is essentially irrelevant to whether the elements are live or static.

These concepts are summarized in the following table.

> 	 	Function               | Live? | Type           | Time Complexity
> 	 	querySelector          |   N   | Element        |  O(n)
> 	 	querySelectorAll       |   N   | NodeList       |  O(n)
> 	 	getElementById         |   Y   | Element        |  O(1)
> 	 	getElementsByClassName |   Y   | HTMLCollection |  O(1)
> 	 	getElementsByTagName   |   Y   | HTMLCollection |  O(1)
> 	 	getElementsByName      |   Y   | NodeList       |  O(1)


[Source and for more detailed information](https://stackoverflow.com/questions/14377590/queryselector-and-queryselectorall-vs-getelementsbyclassname-and-getelementbyid)

## Modifying the DOM.

### Changing the text inside an element.

Given the HTML:

	<p>
		lorem ipsum dolor
	</p>

You can modify its text by first getting the element inside the DOM document and then modifying its inner text:

	cosnt get_p = document.querySelector('p');
	console.log(get_p.innertext)
	**outputs > lorem ipsum dolor**
	get_p.innertext = 'Dummy Text'
	console.log(get_p.innertext)
	**outputs > Dummy Text**


### Changing the HTML inside an element.

*Remember that to change an element in any way you need to reference it*

	const html_mody = document.querySelector('.container > p > b');

	html_mody.innerHTML = '<p> Me duelen las rodillas </p>';

You can also add new content just by making an addition on the referenced Node.

	html_mody.innerHTML += '<p> Me duelen las rodillas </p>';

### Retrieving and Adding/Changing Attributes of HTML elements.

To get an attribute you firstly need to retrieve the node you need, and then use:

	node.getAttribute(attribute_desired)

Example:

	const html_mody = document.querySelector('meta');
	
	console.log(html_mody.getAttribute('charset'))
	**output > utf-8**


To change OR create an Attribute:

	node.setAttribute(attribute_to_modify, new_value)

*The method setAttribute overwrites the attribute in the HTML*

Example:

	const html_mody = document.querySelector('a');

	html_mody.setAttribute('href', 'https://youtube.com')


### Modifying the Style Attribute of a HTML Tag.

A node object has many properties and within that object there is another object called "style":


	const html_mody = document.querySelector('h1')
	**outputs:
			h1:​
				accessKey: ""
				​
				accessKeyLabel: ""
				​
				align: ""
				
				......

And many more, one of those key's is "style" and you can access it and modify it.

Examples:
	
This example modifies the color style of the h1 tag and its background.

*It does not overwrites any previous style!*

	const html_mody = document.querySelector('h1');

	html_mody.style.color = 'orange'
	html_mody.style['background'] = 'black' // Different yet the same


### Adding, Removing and Toggling Classes

You can add/remove classes with the following:

	const html_mody = querySelector('p')

	html_mody.classList.add(class_name)

	html_mody.classList.remove(class_name)

To toggle a class:

	html_mody.classList.toggle(class_name)
	
If the tag has the class it will remove it, if not it will be added without replacing other classes.



	