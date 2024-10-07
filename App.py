from flask import Flask, render_template, request, jsonify
import csv
import random

app = Flask(__name__)

# Sample question database
question_db = {
     'DevOps': {
        'beginner': [
            {'question': "What is CI/CD in DevOps?",
             'options': {'a': 'Code Integration/Code Development',
                         'b': 'Continuous Integration/Continuous Deployment',
                         'c': 'Container Implementation/Cloud Development'},
             'correct_option': 'b'},

            {'question': "Which tool is commonly used for configuration management?",
             'options': {'a': 'Git',
                         'b': 'Docker',
                         'c': 'Ansible'},
             'correct_option': 'c'}
        ],
        'intermediate': [
            {'question': "What is the role of a reverse proxy in DevOps?",
             'options': {'a': 'Security management',
                         'b': 'Load balancing',
                         'c': 'Version control'},
             'correct_option': 'b'},

            {'question': "Which tool is used for container orchestration?",
             'options': {'a': 'Kubernetes',
                         'b': 'Jenkins',
                         'c': 'Terraform'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "How would you implement blue-green deployment?",
             'options': {'a': 'Using separate environments',
                         'b': 'Testing on production',
                         'c': 'Using containers only'},
             'correct_option': 'a'},

            {'question': "Explain infrastructure as code (IaC) and how it applies to DevOps.",
             'options': {'a': 'Manage infrastructure through UI',
                         'b': 'Manage infrastructure through code',
                         'c': 'Automate testing pipelines'},
             'correct_option': 'b'}
        ]
    },
'Mobile App Development': {
        'beginner': [
            {'question': "Which programming language is primarily used for Android app development?",
             'options': {'a': 'Python', 'b': 'Kotlin', 'c': 'Swift'},
             'correct_option': 'b'},
            {'question': "Which programming language is used for iOS app development?",
             'options': {'a': 'Java', 'b': 'Kotlin', 'c': 'Swift'},
             'correct_option': 'c'},
            {'question': "Which Android development framework is built by Google?",
             'options': {'a': 'React Native', 'b': 'Flutter', 'c': 'Ionic'},
             'correct_option': 'b'},
            {'question': "What is the package manager for iOS apps?",
             'options': {'a': 'npm', 'b': 'CocoaPods', 'c': 'Maven'},
             'correct_option': 'b'}
        ],
        'intermediate': [
            {'question': "Which architecture pattern is commonly used in mobile app development?",
             'options': {'a': 'MVC (Model-View-Controller)', 'b': 'Monolithic', 'c': 'Microservices'},
             'correct_option': 'a'},
            {'question': "What is the primary use of Firebase in mobile app development?",
             'options': {'a': 'Database management', 'b': 'Testing', 'c': 'Cloud storage'},
             'correct_option': 'a'},
            {'question': "What is the use of Retrofit in Android development?",
             'options': {'a': 'Dependency Injection', 'b': 'REST API calls', 'c': 'UI rendering'},
             'correct_option': 'b'}
        ],
        'expert': [
            {'question': "How can you implement offline functionality in a mobile app?",
             'options': {'a': 'Using Redux', 'b': 'Using SQLite or Room database', 'c': 'Using NoSQL'},
             'correct_option': 'b'},
            {'question': "Explain the concept of state management in Flutter.",
             'options': {'a': 'Managing variables', 'b': 'Handling asynchronous operations', 'c': 'Managing data and UI interaction'},
             'correct_option': 'c'},
            {'question': "How do you manage app security in mobile development?",
             'options': {'a': 'By adding encryption and obfuscation', 'b': 'By using Firebase', 'c': 'Using CI/CD'},
             'correct_option': 'a'}
        ]
    },

    'Cybersecurity': {
        'beginner': [
            {'question': "What is the primary objective of cybersecurity?",
             'options': {'a': 'Data confidentiality, integrity, availability', 'b': 'Monitoring network traffic', 'c': 'Hacking into systems'},
             'correct_option': 'a'},
            {'question': "Which of the following is a strong password?",
             'options': {'a': 'password123', 'b': 'abc', 'c': 'R@nd0m!9'},
             'correct_option': 'c'},
            {'question': "What does VPN stand for?",
             'options': {'a': 'Virtual Private Network', 'b': 'Very Private Network', 'c': 'Virtual Public Network'},
             'correct_option': 'a'},
            {'question': "Which type of attack is phishing?",
             'options': {'a': 'Social engineering', 'b': 'DDoS', 'c': 'Man-in-the-middle'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "What is a firewall?",
             'options': {'a': 'Hardware to prevent overheating', 'b': 'System to monitor and control network traffic', 'c': 'A virus scanning tool'},
             'correct_option': 'b'},
            {'question': "Which of the following is an example of encryption?",
             'options': {'a': 'AES-256', 'b': 'MD5', 'c': 'HTTP'},
             'correct_option': 'a'},
            {'question': "What is a zero-day vulnerability?",
             'options': {'a': 'A vulnerability that is already patched', 'b': 'An undisclosed vulnerability', 'c': 'A vulnerability discovered years ago'},
             'correct_option': 'b'}
        ],
        'expert': [
            {'question': "How would you defend against a DDoS attack?",
             'options': {'a': 'Using load balancers', 'b': 'Using a VPN', 'c': 'Using firewalls'},
             'correct_option': 'a'},
            {'question': "What is a penetration test?",
             'options': {'a': 'An audit of network performance', 'b': 'An authorized simulated attack', 'c': 'A test to scan for vulnerabilities'},
             'correct_option': 'b'},
            {'question': "What is the principle of least privilege?",
             'options': {'a': 'Give minimal access to systems', 'b': 'Give admin access to all', 'c': 'Lock down systems completely'},
             'correct_option': 'a'}
        ]
    },

    'IOT': {
        'beginner': [
            {'question': "What does IoT stand for?",
             'options': {'a': 'Internet of Things', 'b': 'Internet on Time', 'c': 'Intranet of Things'},
             'correct_option': 'a'},
            {'question': "Which of the following is an example of an IoT device?",
             'options': {'a': 'Smart thermostat', 'b': 'Desktop computer', 'c': 'USB drive'},
             'correct_option': 'a'},
            {'question': "What communication protocol is commonly used in IoT?",
             'options': {'a': 'HTTP', 'b': 'MQTT', 'c': 'SMTP'},
             'correct_option': 'b'},
            {'question': "What is an IoT gateway?",
             'options': {'a': 'A device that connects sensors to the cloud', 'b': 'A firewall', 'c': 'A router'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "Which type of network is most commonly used in IoT?",
             'options': {'a': 'LAN', 'b': 'Wi-Fi', 'c': 'LoRaWAN'},
             'correct_option': 'c'},
            {'question': "Which sensor is used to measure temperature in IoT devices?",
             'options': {'a': 'Thermocouple', 'b': 'Ultrasonic sensor', 'c': 'Infrared sensor'},
             'correct_option': 'a'},
            {'question': "What is the role of edge computing in IoT?",
             'options': {'a': 'Process data close to the source', 'b': 'Send data to the cloud', 'c': 'Monitor network traffic'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is fog computing in IoT?",
             'options': {'a': 'Data processing at the edge of the network', 'b': 'A form of cloud storage', 'c': 'Data collection via drones'},
             'correct_option': 'a'},
            {'question': "Which type of network attack is most common in IoT?",
             'options': {'a': 'Man-in-the-middle', 'b': 'Phishing', 'c': 'Eavesdropping'},
             'correct_option': 'a'},
            {'question': "What is an IoT analytics platform?",
             'options': {'a': 'A tool to analyze data from IoT devices', 'b': 'A database for storing IoT data', 'c': 'A firewall for IoT devices'},
             'correct_option': 'a'}
        ]
    },

    'Software Engineering': {
        'beginner': [
            {'question': "What is the primary goal of software engineering?",
             'options': {'a': 'Developing hardware', 'b': 'Writing code', 'c': 'Designing, developing, and maintaining software'},
             'correct_option': 'c'},
            {'question': "What is an SDLC?",
             'options': {'a': 'Software Design Language Concept', 'b': 'Software Development Life Cycle', 'c': 'System Debugging Lifecycle'},
             'correct_option': 'b'},
            {'question': "Which of the following is an Agile methodology?",
             'options': {'a': 'Waterfall', 'b': 'Scrum', 'c': 'V-model'},
             'correct_option': 'b'},
            {'question': "What does a version control system help with?",
             'options': {'a': 'Storing old versions of code', 'b': 'Collaborative development', 'c': 'Generating reports'},
             'correct_option': 'b'}
        ],
        'intermediate': [
            {'question': "Which design pattern is used to ensure only one instance of a class exists?",
             'options': {'a': 'Factory', 'b': 'Singleton', 'c': 'Builder'},
             'correct_option': 'b'},
            {'question': "What is the purpose of a Unit Test?",
             'options': {'a': 'Test the entire software system', 'b': 'Test individual components or functions', 'c': 'Ensure the software meets the customer’s needs'},
             'correct_option': 'b'},
            {'question': "What is a REST API?",
             'options': {'a': 'A type of API that uses HTTP requests', 'b': 'A backend service', 'c': 'A database connection'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is the purpose of Continuous Integration?",
             'options': {'a': 'To integrate testing environments', 'b': 'To enable constant bug tracking', 'c': 'To merge code regularly and test automatically'},
             'correct_option': 'c'},
            {'question': "What is microservices architecture?",
             'options': {'a': 'A single monolithic application', 'b': 'A system broken down into independent, modular services', 'c': 'A type of database design'},
             'correct_option': 'b'},
            {'question': "Which tool is commonly used for DevOps automation?",
             'options': {'a': 'Kubernetes', 'b': 'GIT', 'c': 'Jenkins'},
             'correct_option': 'c'}
        ]
    },

    'Data Science': {
        'beginner': [
            {'question': "Which of the following is used for data analysis?",
             'options': {'a': 'Excel', 'b': 'Photoshop', 'c': 'Premiere Pro'},
             'correct_option': 'a'},
            {'question': "What is a DataFrame?",
             'options': {'a': 'A table-like structure in Python for managing data', 'b': 'A form of a database', 'c': 'A type of chart'},
             'correct_option': 'a'},
            {'question': "What is a common data visualization library in Python?",
             'options': {'a': 'Matplotlib', 'b': 'Scikit-learn', 'c': 'NumPy'},
             'correct_option': 'a'},
            {'question': "Which of the following is a supervised learning algorithm?",
             'options': {'a': 'K-Means', 'b': 'Linear Regression', 'c': 'Principal Component Analysis'},
             'correct_option': 'b'}
        ],
        'intermediate': [
            {'question': "Which Python library is used for data manipulation and cleaning?",
             'options': {'a': 'Pandas', 'b': 'Scikit-learn', 'c': 'PyTorch'},
             'correct_option': 'a'},
            {'question': "What is the purpose of feature engineering in data science?",
             'options': {'a': 'To train models', 'b': 'To prepare and improve data for model building', 'c': 'To visualize data'},
             'correct_option': 'b'},
            {'question': "What is a confusion matrix used for?",
             'options': {'a': 'Visualize decision trees', 'b': 'Analyze classification model performance', 'c': 'Represent neural network layers'},
             'correct_option': 'b'}
        ],
        'expert': [
            {'question': "What is the curse of dimensionality?",
             'options': {'a': 'A large number of features affecting the performance of machine learning models', 'b': 'A problem of too much data to handle', 'c': 'A security issue with databases'},
             'correct_option': 'a'},
            {'question': "What is hyperparameter tuning?",
             'options': {'a': 'Optimizing the parameters during model training', 'b': 'Choosing the best model architecture', 'c': 'Adjusting model complexity'},
             'correct_option': 'a'},
            {'question': "Which algorithm is most suited for imbalanced data?",
             'options': {'a': 'Random Forest', 'b': 'SMOTE (Synthetic Minority Oversampling)', 'c': 'K-Means'},
             'correct_option': 'b'}
        ]
    },

    'Cloud Computing': {
        'beginner': [
            {'question': "What does IaaS stand for?",
             'options': {'a': 'Infrastructure as a Service', 'b': 'Internet as a Service', 'c': 'Information as a Service'},
             'correct_option': 'a'},
            {'question': "Which of the following is a cloud platform?",
             'options': {'a': 'AWS', 'b': 'Photoshop', 'c': 'Windows'},
             'correct_option': 'a'},
            {'question': "What is virtualization in cloud computing?",
             'options': {'a': 'Creating virtual versions of hardware', 'b': 'Using servers', 'c': 'Connecting networks'},
             'correct_option': 'a'},
            {'question': "What does SaaS stand for?",
             'options': {'a': 'System as a Software', 'b': 'Software as a Service', 'c': 'Server as a Solution'},
             'correct_option': 'b'}
        ],
        'intermediate': [
            {'question': "What is a cloud region?",
             'options': {'a': 'A physical location where data centers reside', 'b': 'A type of cloud storage', 'c': 'A type of cloud network'},
             'correct_option': 'a'},
            {'question': "Which of the following is a benefit of cloud computing?",
             'options': {'a': 'Increased hardware cost', 'b': 'Scalability and flexibility', 'c': 'Slower performance'},
             'correct_option': 'b'},
            {'question': "What is Kubernetes?",
             'options': {'a': 'A container orchestration platform', 'b': 'A cloud provider', 'c': 'A machine learning tool'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is a serverless architecture?",
             'options': {'a': 'A network without servers', 'b': 'A cloud architecture where you only focus on code execution', 'c': 'An architecture with minimal servers'},
             'correct_option': 'b'},
            {'question': "What is multi-tenancy in cloud?",
             'options': {'a': 'Sharing resources among multiple customers', 'b': 'Using a single user per server', 'c': 'Running a private cloud'},
             'correct_option': 'a'},
            {'question': "How do you ensure high availability in the cloud?",
             'options': {'a': 'Using RAID storage', 'b': 'Implementing multi-region architecture', 'c': 'Increasing the server size'},
             'correct_option': 'b'}
        ]
    },

    'Machine Learning': {
        'beginner': [
            {'question': "Which of the following is an example of supervised learning?",
             'options': {'a': 'Clustering', 'b': 'Classification', 'c': 'PCA'},
             'correct_option': 'b'},
            {'question': "What is a feature in machine learning?",
             'options': {'a': 'A row in the dataset', 'b': 'A column in the dataset', 'c': 'A class label'},
             'correct_option': 'b'},
            {'question': "Which algorithm is used for regression tasks?",
             'options': {'a': 'Logistic regression', 'b': 'Linear regression', 'c': 'Random forest'},
             'correct_option': 'b'},
            {'question': "What is overfitting?",
             'options': {'a': 'When a model fits the training data too well and performs poorly on new data', 'b': 'When a model performs poorly on training data', 'c': 'A type of neural network'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "Which regularization technique penalizes the magnitude of coefficients in linear models?",
             'options': {'a': 'Lasso', 'b': 'Random Forest', 'c': 'K-means'},
             'correct_option': 'a'},
            {'question': "What is cross-validation used for?",
             'options': {'a': 'Improving model architecture', 'b': 'Evaluating model performance on unseen data', 'c': 'Reducing computation time'},
             'correct_option': 'b'},
            {'question': "Which of the following is an unsupervised learning algorithm?",
             'options': {'a': 'K-Means', 'b': 'Logistic Regression', 'c': 'Support Vector Machine'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is a convolutional neural network (CNN) primarily used for?",
             'options': {'a': 'Image processing tasks', 'b': 'Text analysis', 'c': 'Time series analysis'},
             'correct_option': 'a'},
            {'question': "What is transfer learning?",
             'options': {'a': 'A technique where a pre-trained model is adapted to a new task', 'b': 'A form of unsupervised learning', 'c': 'A method of clustering'},
             'correct_option': 'a'},
            {'question': "What is gradient descent?",
             'options': {'a': 'A method to update model weights during training', 'b': 'A method to increase learning rate', 'c': 'A clustering technique'},
             'correct_option': 'a'}
        ]
    },

    'AI': {
        'beginner': [
            {'question': "What is artificial intelligence?",
             'options': {'a': 'Simulating human intelligence in machines', 'b': 'Programming languages', 'c': 'Creating virtual reality environments'},
             'correct_option': 'a'},
            {'question': "Which of the following is an application of AI?",
             'options': {'a': 'Autonomous vehicles', 'b': 'Word processors', 'c': 'Image editing software'},
             'correct_option': 'a'},
            {'question': "What does NLP stand for in AI?",
             'options': {'a': 'Natural Language Processing', 'b': 'Neural Learning Protocol', 'c': 'Node-based Logic Program'},
             'correct_option': 'a'},
            {'question': "Which of the following is an example of a weak AI system?",
             'options': {'a': 'Chatbot', 'b': 'Autonomous car', 'c': 'General AI'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "What is the difference between supervised and unsupervised learning?",
             'options': {'a': 'Supervised learning uses labeled data, unsupervised does not', 'b': 'Supervised learning is faster', 'c': 'Unsupervised learning is always better for large datasets'},
             'correct_option': 'a'},
            {'question': "What is reinforcement learning?",
             'options': {'a': 'A type of learning where agents learn by trial and error', 'b': 'A form of supervised learning', 'c': 'A method to train neural networks'},
             'correct_option': 'a'},
            {'question': "What is an artificial neural network?",
             'options': {'a': 'A model inspired by biological neurons for processing data', 'b': 'A rule-based expert system', 'c': 'A type of clustering algorithm'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is deep learning?",
             'options': {'a': 'A subset of machine learning involving neural networks with many layers', 'b': 'A form of weak AI', 'c': 'A type of supervised learning'},
             'correct_option': 'a'},
            {'question': "What is a generative adversarial network (GAN)?",
             'options': {'a': 'A neural network architecture for generating new data', 'b': 'A reinforcement learning algorithm', 'c': 'An optimization technique'},
             'correct_option': 'a'},
            {'question': "What is the Turing Test?",
             'options': {'a': 'A test to determine if a machine exhibits human-like intelligence', 'b': 'A test for computer performance', 'c': 'A test for autonomous systems'},
             'correct_option': 'a'}
        ]
    },

    'UI/UX Design': {
        'beginner': [
            {'question': "What does UI stand for?",
             'options': {'a': 'User Interface', 'b': 'Unified Integration', 'c': 'Unique Identity'},
             'correct_option': 'a'},
            {'question': "What does UX stand for?",
             'options': {'a': 'User Experience', 'b': 'Utility Example', 'c': 'Unit Exchange'},
             'correct_option': 'a'},
            {'question': "Which of the following is a tool commonly used for UI design?",
             'options': {'a': 'Sketch', 'b': 'GitHub', 'c': 'Google Analytics'},
             'correct_option': 'a'},
            {'question': "What is a wireframe?",
             'options': {'a': 'A low-fidelity representation of a design', 'b': 'A backend framework', 'c': 'A network diagram'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "Which of the following is a key principle of UX design?",
             'options': {'a': 'Consistency', 'b': 'Colorful design', 'c': 'High-fidelity prototyping'},
             'correct_option': 'a'},
            {'question': "What is a user persona?",
             'options': {'a': 'A fictional representation of your ideal user', 'b': 'A color scheme', 'c': 'A type of UI component'},
             'correct_option': 'a'},
            {'question': "Which term describes testing a product with real users?",
             'options': {'a': 'Usability testing', 'b': 'A/B testing', 'c': 'Regression testing'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is a design system?",
             'options': {'a': 'A collection of reusable UI components and guidelines', 'b': 'A UI framework', 'c': 'A system for coding websites'},
             'correct_option': 'a'},
            {'question': "What is the difference between UX and UI?",
             'options': {'a': 'UI focuses on visual design, UX focuses on the overall experience', 'b': 'UX is for developers, UI is for designers', 'c': 'They are the same'},
             'correct_option': 'a'},
            {'question': "What is the goal of a UX audit?",
             'options': {'a': 'To identify usability issues in a product', 'b': 'To design new features', 'c': 'To change the color scheme'},
             'correct_option': 'a'}
        ]
    },

    'Blockchain': {
        'beginner': [
            {'question': "What is a blockchain?",
             'options': {'a': 'A decentralized ledger of transactions', 'b': 'A cloud storage platform', 'c': 'A form of currency'},
             'correct_option': 'a'},
            {'question': "Which of the following is a key feature of blockchain?",
             'options': {'a': 'Immutability', 'b': 'Centralized control', 'c': 'Scalability'},
             'correct_option': 'a'},
            {'question': "What is Bitcoin?",
             'options': {'a': 'A cryptocurrency', 'b': 'A blockchain framework', 'c': 'A web browser'},
             'correct_option': 'a'},
            {'question': "What is the process of verifying transactions in blockchain called?",
             'options': {'a': 'Mining', 'b': 'Sorting', 'c': 'Hashing'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "What is a smart contract?",
             'options': {'a': 'A self-executing contract with the terms directly written into code', 'b': 'A legal agreement', 'c': 'A security protocol'},
             'correct_option': 'a'},
            {'question': "Which of the following is a blockchain platform?",
             'options': {'a': 'Ethereum', 'b': 'Google Cloud', 'c': 'Linux'},
             'correct_option': 'a'},
            {'question': "What is a consensus algorithm?",
             'options': {'a': 'A protocol to ensure all nodes agree on a single version of the blockchain', 'b': 'A mining technique', 'c': 'A way to encrypt transactions'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is the role of a Merkle Tree in blockchain?",
             'options': {'a': 'To efficiently and securely verify the integrity of data', 'b': 'To store transactions', 'c': 'To create new blocks'},
             'correct_option': 'a'},
            {'question': "What is proof of stake?",
             'options': {'a': 'A consensus algorithm where validators are chosen based on the number of coins they hold', 'b': 'A method of mining blocks', 'c': 'A security protocol'},
             'correct_option': 'a'},
            {'question': "What is the primary purpose of a blockchain fork?",
             'options': {'a': 'To split a blockchain into two versions', 'b': 'To optimize transaction speed', 'c': 'To create new cryptocurrency'},
             'correct_option': 'a'}
        ]
    },

    'Web Development': {
        'beginner': [
            {'question': "Which language is used for the structure of web pages?",
             'options': {'a': 'HTML', 'b': 'JavaScript', 'c': 'Python'},
             'correct_option': 'a'},
            {'question': "What does CSS stand for?",
             'options': {'a': 'Cascading Style Sheets', 'b': 'Colorful Style Sheets', 'c': 'Cascading System Sheets'},
             'correct_option': 'a'},
            {'question': "Which language is used to make web pages interactive?",
             'options': {'a': 'HTML', 'b': 'JavaScript', 'c': 'CSS'},
             'correct_option': 'b'},
            {'question': "What is a responsive web design?",
             'options': {'a': 'A design that adapts to different screen sizes', 'b': 'A static web page', 'c': 'A dynamic web page'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "Which of the following is a front-end JavaScript framework?",
             'options': {'a': 'React', 'b': 'Django', 'c': 'Laravel'},
             'correct_option': 'a'},
            {'question': "What is an API?",
             'options': {'a': 'A set of tools for building software applications', 'b': 'A web server', 'c': 'A database language'},
             'correct_option': 'a'},
            {'question': "What is the purpose of a web server?",
             'options': {'a': 'To store data', 'b': 'To serve web pages to clients', 'c': 'To compile code'},
             'correct_option': 'b'}
        ],
        'expert': [
            {'question': "What is the role of a web socket?",
             'options': {'a': 'To provide full-duplex communication over a single TCP connection', 'b': 'To secure data between a server and a client', 'c': 'To cache web pages'},
             'correct_option': 'a'},
            {'question': "What is server-side rendering?",
             'options': {'a': 'Rendering a web page on the server before sending it to the client', 'b': 'A type of API request', 'c': 'Caching data in the browser'},
             'correct_option': 'a'},
            {'question': "Which of the following is a common backend language?",
             'options': {'a': 'Node.js', 'b': 'JavaScript', 'c': 'React'},
             'correct_option': 'a'}
        ]
    },

    'Cybersecurity': {
        'beginner': [
            {'question': "What is cybersecurity?",
             'options': {'a': 'Protecting systems and networks from digital attacks', 'b': 'Creating software', 'c': 'Building networks'},
             'correct_option': 'a'},
            {'question': "Which of the following is a common cybersecurity threat?",
             'options': {'a': 'Phishing', 'b': 'Database indexing', 'c': 'Server rendering'},
             'correct_option': 'a'},
            {'question': "What does encryption do?",
             'options': {'a': 'Secures data by converting it into an unreadable format', 'b': 'Compresses files', 'c': 'Sends emails securely'},
             'correct_option': 'a'},
            {'question': "What is a firewall?",
             'options': {'a': 'A security system that controls incoming and outgoing network traffic', 'b': 'A web server', 'c': 'A software update'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "What is multi-factor authentication?",
             'options': {'a': 'A method requiring more than one form of authentication to access a system', 'b': 'A type of encryption', 'c': 'A type of malware'},
             'correct_option': 'a'},
            {'question': "What is a zero-day vulnerability?",
             'options': {'a': 'A security flaw that is exploited before the vendor has issued a patch', 'b': 'A type of encryption', 'c': 'A type of firewall'},
             'correct_option': 'a'},
            {'question': "What is a penetration test?",
             'options': {'a': 'A test to identify security weaknesses in a system', 'b': 'A load test for servers', 'c': 'A test to verify encryption'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is social engineering?",
             'options': {'a': 'Manipulating people into giving up confidential information', 'b': 'Hacking a server', 'c': 'A type of phishing attack'},
             'correct_option': 'a'},
            {'question': "What is the purpose of a VPN?",
             'options': {'a': 'To create a secure connection to another network over the internet', 'b': 'To encrypt files', 'c': 'To filter network traffic'},
             'correct_option': 'a'},
            {'question': "What is the difference between a virus and a worm?",
             'options': {'a': 'A virus needs a host file to spread, a worm can replicate itself without a host', 'b': 'A worm needs a host, a virus doesn’t', 'c': 'They are the same'},
             'correct_option': 'a'}
        ]
    },

    'Spiking Neural Networks': {
        'beginner': [
            {'question': "What is a spiking neural network?",
             'options': {'a': 'A type of neural network that mimics the way biological neurons communicate using spikes', 'b': 'A deep learning algorithm', 'c': 'A form of supervised learning'},
             'correct_option': 'a'},
            {'question': "Which of the following is a spiking neuron model?",
             'options': {'a': 'Leaky Integrate-and-Fire', 'b': 'Convolutional neuron', 'c': 'Logistic neuron'},
             'correct_option': 'a'},
            {'question': "What is spike-timing-dependent plasticity (STDP)?",
             'options': {'a': 'A learning rule based on the timing of spikes between neurons', 'b': 'A type of backpropagation', 'c': 'A clustering algorithm'},
             'correct_option': 'a'},
            {'question': "What is the primary advantage of spiking neural networks?",
             'options': {'a': 'Energy efficiency and biological plausibility', 'b': 'Faster training', 'c': 'More accurate than other neural networks'},
             'correct_option': 'a'}
        ],
        'intermediate': [
            {'question': "Which encoding method is commonly used in spiking neural networks?",
             'options': {'a': 'Rate coding', 'b': 'One-hot encoding', 'c': 'Word embeddings'},
             'correct_option': 'a'},
            {'question': "What is a key challenge in training spiking neural networks?",
             'options': {'a': 'The non-differentiability of spike events', 'b': 'Data preprocessing', 'c': 'Gradient vanishing problem'},
             'correct_option': 'a'},
            {'question': "How do spiking neural networks differ from traditional artificial neural networks?",
             'options': {'a': 'SNNs use discrete spike events while traditional ANNs use continuous activation functions', 'b': 'SNNs are faster', 'c': 'SNNs require more data'},
             'correct_option': 'a'}
        ],
        'expert': [
            {'question': "What is the role of the membrane potential in spiking neurons?",
             'options': {'a': 'It determines whether the neuron will fire a spike', 'b': 'It is used for weight updating', 'c': 'It controls the learning rate'},
             'correct_option': 'a'},
            {'question': "Which of the following is a neuromorphic hardware platform for running spiking neural networks?",
             'options': {'a': 'Loihi', 'b': 'TensorFlow', 'c': 'PyTorch'},
             'correct_option': 'a'},
            {'question': "What is the concept of homeostasis in SNNs?",
             'options': {'a': 'A regulatory mechanism to maintain stable activity levels in the network', 'b': 'A way to encode information', 'c': 'A method of weight initialization'},
             'correct_option': 'a'}
        ]
    }
}

# Fetch questions for a course
@app.route('/get_questions', methods=['GET'])
def get_questions():
    course_interest = request.args.get('course')
    if course_interest in question_db:
        questions = []
        for level in ['beginner', 'intermediate', 'expert']:
            questions.extend(question_db[course_interest][level])
        return jsonify(questions)
    return jsonify([]), 404

# Function to determine the user's skill level based on the score
def determine_skill_level(score):
    if score <= 2:
        return "beginner"
    elif 3 <= score <= 5:
        return "intermediate"
    else:
        return "expert"


def recommend_modules(course_interest, skill_level, csv_file='all_courses_updated_dataset.csv'):
    recommended_modules = []

    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['course_name'] == course_interest:
                if skill_level == 'beginner' and row['difficulty_level'] in ['easy', 'medium', 'hard']:
                    recommended_modules.append(row)
                elif skill_level == 'intermediate' and row['difficulty_level'] in ['medium', 'hard']:
                    recommended_modules.append(row)
                elif skill_level == 'expert' and row['difficulty_level'] == 'hard':
                    recommended_modules.append(row)

    return recommended_modules

# Route to handle quiz submission and return skill level + recommendations
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    course_interest = data['course']
    user_answers = data['answers']

    score = 0
    for answer in user_answers:
        if answer['user_option'] == answer['correct_option']:
            score += 1

    skill_level = determine_skill_level(score)

    
    recommended = recommend_modules(course_interest, skill_level)
    return jsonify({
        'skill_level': skill_level,
        'recommended_modules': recommended,
        'score': score  
    })

@app.route('/')
def index():
    return render_template('index.html',recommended=recommended)

if __name__ == '__main__':
    app.run(debug=True)
