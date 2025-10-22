resource "azurerm_kubernetes_cluster" "supra_cluster" {
  name                = "supra-intelligence"
  location            = azurerm_resource_group.gracealone.location
  resource_group_name = azurerm_resource_group.gracealone.name
  dns_prefix          = "supraintel"
  default_node_pool {
    name       = "supra"
    node_count = 5
    vm_size    = "Standard_B4ms"
  }
  identity {
    type = "SystemAssigned"
  }
}
