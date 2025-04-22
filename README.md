# Online Shop API  

This is an Online Shop API built with Django REST Framework. The API provides functionality for managing products, users, orders, and more, allowing for a full-featured online shopping experience.  


## Features  
- User registration and authentication  
- Product management (CRUD operations)  
- Order management  
- Search and filter products  


## Technologies Used  

- **Django**  
- **Django REST Framework**  
- **drf-nested-routers**  
- **django-filter**  
- **Djoser**  
- **djangorestframework-simplejwt**  
- **factory-boy**  
- **Faker**  


## Getting Started with Docker  

This project is fully dockerized for easy development and deployment. 



## Performance Optimizations  

This project has been optimized for performance with the following strategies:  

1. **Database Query Optimization**:  
   - All critical queries are indexed to enhance retrieval times.  
   - Used some orm optimization by `prefetch_class`, `prefetch_related`, `select_related` and other to minimize database hits during operations involving related entities.  


2. **Benchmark Results**:  
   - Initial loading times have decreased by over 60% compared to earlier versions
  



