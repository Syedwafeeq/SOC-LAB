# WAZUH-UBUNTU-END Configuration

This directory contains configuration files and setup components for the Wazuh Ubuntu endpoint.

## 📌 Note on TheHive Configuration

Although **TheHive** is logically part of this setup, its configuration folder (`THEHIVE`) is placed outside this directory in the repository structure.

### 💡 Why is THEHIVE outside?

For better clarity and organization:

* The `THEHIVE` directory is kept separate to **avoid deep nesting**
* This makes the repository structure **cleaner and easier to navigate**
* It allows users to **quickly locate and understand components independently**

### 🔁 Logical Structure

In a more compact structure, it could have been organized like this:

```
WAZUH-UBUNTU-END/
├── THEHIVE/
├── other-configs/
```

However, for readability and maintainability, it is structured as:

```
CONFIGS/
├── WAZUH-UBUNTU-END/
├── THEHIVE/
```

## ✅ Summary

* `THEHIVE` is part of the overall system setup
* It is intentionally placed outside this folder for **better structure and clarity**

---

Feel free to explore both directories together to understand the full configuration.
