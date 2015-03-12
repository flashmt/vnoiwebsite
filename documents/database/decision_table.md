##Decision Table

| Model       | Admin | User | Visitor |
|: ----------:|:------:| :------:|:------:|
| ForumGroup| CRUD | R | R | 
| Forum     | CRUD | R | R | 
| Topic | CRUD | CR,U(owner) | R | 
| Post | CRUD | CR, U(owner) | R | 
| Vote | CRUD | CR | R | 
| User | CRUD | CR,U(owner) | R | 
| Message | CRUD | CR,D(owner) | R | 


###Notes
- Create: Create a model instance
- Retrieve: Access information of a model instance.
- Update: Change information of a model instance
- Delete: Delete a model instance
