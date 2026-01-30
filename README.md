# Mendeleev: Professional Interactive Periodic Table Platform

Mendeleev is an advanced digital platform and comprehensive educational tool designed for the detailed study of the 118 chemical elements of the periodic table. This project serves as a high-fidelity alternative to static educational materials, offering a dynamic environment where users can interact with chemical data in real-time. The platform is engineered to meet the needs of students, academic researchers, and chemistry professionals by providing accurate scientific parameters and visual simulations.

### 🌐 [Access the Live Demonstration](https://adfchcjnkb.github.io/periodic-table/)

---

<p align="center">
  <img src="https://img.shields.io/badge/Environment-Production-00d4ff?style=for-the-badge" alt="Production">
  <img src="https://img.shields.io/badge/Architecture-Single_Page_Application-ff2a6d?style=for-the-badge" alt="Architecture">
  <img src="https://img.shields.io/badge/Core_Engine-Vanilla_JavaScript-yellow?style=for-the-badge" alt="JS">
  <img src="https://img.shields.io/badge/UI_Style-Modern_Rounded_Animations-06d6a0?style=for-the-badge" alt="UI">
</p>

---

## 📖 Comprehensive Project Documentation

The Mendeleev project is built on the principle of "Information Density with Visual Clarity." In the field of chemistry, the relationship between elements is as important as the elements themselves. This platform recreates the IUPAC-standard periodic table grid, ensuring that every period and group is correctly aligned. The user interface is designed using modern CSS standards, where every element possesses rounded borders (Border Radius) and interactive feedback loops.

### 🛠 Development Status & Future Roadmap

We follow a rigorous development cycle to ensure the platform evolves with modern web standards.

1.  **Backend Integration (Active Development):** 
    The current version operates as a high-performance static application. We are currently developing a dedicated backend infrastructure. This future update will transition the project into a full-stack application, enabling dynamic data management, user profiles, and advanced server-side processing.
    
2.  **Bilingual Support (Upcoming Phase):** 
    At this stage, the platform’s primary language is Persian. We are in the process of implementing a localization system. In the near future, the application will fully support the English language, allowing users to toggle between Persian and English interfaces seamlessly.

3.  **Cross-Platform Performance:** 
    The code is optimized for various browsers (Chrome, Firefox, Safari, Edge), ensuring consistent behavior of animations and data rendering across all platforms.

---

## 🔍 In-Depth Feature Analysis

### 1. Primary Interface and Grid Systems
The main dashboard displays the elements in an organized 18-column grid. Each cell is a self-contained unit of information showing the Atomic Number, Chemical Symbol, and Persian Name.
- **Interactive UI Design:** In the software environment, every cell is programmed with rounded corners. We have implemented a "Hover Animation" system: when the cursor moves over a cell, the element scales up slightly and a glowing border effect is activated, improving user focus.
- **Chemical Grouping:** Elements are automatically categorized into groups such as Alkali Metals, Transition Metals, Lanthanides, and Actinides. Each group has a distinct color code for immediate identification.

<p align="center">
  <img src="https://raw.githubusercontent.com/adfchcjnkb/periodic-table/refs/heads/main/main%20page%20(Desktop)%20.png" width="90%" alt="Main Desktop Interface">
</p>

### 2. Advanced Atomic Bohr Simulation
One of the most significant technical components of this project is the real-time visualization of the Bohr atomic model.
- **Mathematical Logic:** The application calculates the electron distribution for each shell (K, L, M, N, O, P, Q) based on the element's atomic number.
- **Dynamic Animation:** Electrons are not static; they are programmed to rotate around the nucleus in constant circular motion. This provides a clear understanding of the element's electronic structure.
- **Data Detail:** When a user clicks on an element, a side panel displays extensive information, including Atomic Mass, total protons, neutrons, discovery year, and a list of industrial and scientific applications.

<p align="center">
  <img src="https://raw.githubusercontent.com/adfchcjnkb/periodic-table/refs/heads/main/atomic%20model.png" width="60%" alt="Atomic Bohr Model Visualization">
</p>

### 3. Responsive Mobile Engineering
Recognizing that many users access educational tools via mobile devices, we have implemented a comprehensive responsive design strategy.
- **Adaptive Layouts:** The layout shifts dynamically based on screen resolution. On smaller screens, the periodic table utilizes a smooth horizontal scroll system.
- **Touch Optimization:** All interactive elements, including rounded buttons and element cells, are optimized for touch input, ensuring that mobile users have the same high-quality experience as desktop users.

<p align="center">
  <img src="https://raw.githubusercontent.com/adfchcjnkb/periodic-table/refs/heads/main/main%20page%20(mobile)%20.png" width="35%" alt="Mobile Responsive View">
</p>

### 4. Project Documentation (About Us)
The "About" page serves as the official documentation of the team's goals and the technical history of the platform. It outlines the educational mission and provides contact information for the development leads.

<p align="center">
  <img src="https://raw.githubusercontent.com/adfchcjnkb/periodic-table/refs/heads/main/about%20page%20(Desktop)%20.png" width="90%" alt="About Us Page">
</p>

---

## 💻 Technical Stack and Architecture

### **Core Frontend Technologies**
| Technology | Implementation |
| :--- | :--- |
| **HTML5** | Used for structured data representation and semantic accessibility. |
| **CSS3** | Implements the grid system, rounded corner styling, and all transition/hover animations. |
| **JavaScript (ES6+)** | Manages the application logic, real-time search filtering, and the atomic model calculations. |

### **Information Architecture**
The scientific data is organized into optimized JSON structures. This allows the application to perform instant searches across 118 elements without any delay. The search algorithm is designed to match queries against atomic numbers, symbols, and element names simultaneously.

---

## 👥 Development and Contribution

The development of this project is managed by a specialized team focused on chemistry and software engineering.

- **Arvin Kheradmand:** Lead Designer and Frontend Developer. Responsible for the UI/UX architecture, visual animations, and responsive systems.
- **Hosein Yarmohammadi:** System Logic Architect and Backend Developer. Responsible for data integrity, core application logic, and backend infrastructure development.

---

## 📑 Detailed Project Specifications

- **Animations:** All interactive components use CSS `transition` and `transform` properties for smooth 60fps performance.
- **Borders:** A consistent `border-radius` policy is applied to all cards, panels, and input fields to maintain a modern aesthetic.
- **Search Logic:** Case-insensitive search with support for Persian characters and numeric atomic numbers.
- **Copyright:** All scientific data and code structures are managed under the Mendeleev Project Group (2026).

---
<p align="center">
  For further technical inquiries or collaboration, please contact the development team via official channels.
</p>
