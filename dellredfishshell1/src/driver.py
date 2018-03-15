# dellredfishshell1 driver
#
# _author_ = Jiim Brannan <jim.b@quali.com>
# _version_ = 2.0

from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.core.logger import qs_logger
import requests, json, sys, subprocess, os, datetime
import warnings
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, AutoLoadResource, \
    AutoLoadAttribute, AutoLoadDetails, CancellationContext
#from data_model import *  # run 'shellfoundry generate' to generate data model classes
from cloudshell.api.cloudshell_api import CloudShellAPISession


class Dellredfishshell1Driver(ResourceDriverInterface):

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        pass


    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        warnings.filterwarnings("ignore")
        self.logger = qs_logger.get_qs_logger('Canvas',context.resource.name)
        self.logger.info(str(context.resource.attributes))
        self.resourcename = context.resource.name
        self.resourceaddress = context.resource.address
        self.idrac_ip = context.resource.attributes['Dellredfishshell1.iDRAC_ip']
        self.idrac_username = context.resource.attributes['Dellredfishshell1.iDRAC_username']
        api = CloudShellSessionContext(context).get_api()
        self.idrac_password = \
            api.DecryptPassword(context.resource.attributes['Dellredfishshell1.iDRAC_password']).Value
        self.logger.info(
            "idrac: ip {0}, user {1}, pass {2}".format(self.idrac_ip, self.idrac_username, self.idrac_password))


    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    # <editor-fold desc="Discovery">

    def get_inventory(self, context):
        """
        Discovers the resource structure and attributes.
        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """
        # See below some example code demonstrating how to return the resource structure and attributes
        # In real life, this code will be preceded by SNMP/other calls to the resource details and will not be static
        # run 'shellfoundry generate' in order to create classes that represent your data model

        #resource = DellRedfishShell1Driver.create_from_context(context)
        #resource.vendor = 'Dell'
        #resource.model = 'Dell Generic'
        #port1 = ResourcePort('Port 1')
        #port1.ipv4_address = '192.168.10.7'
        #resource.add_sub_resource('1', port1)

        #return resource.create_autoload_details()
        pass

    # </editor-fold>

    # <editor-fold desc="Orchestration Save and Restore Standard">
    def orchestration_save(self, context, cancellation_context, mode, custom_params):
        """
        Saves the Shell state and returns a description of the saved artifacts and information
        This command is intended for API use only by sandbox orchestration scripts to implement
        a save and restore workflow
        :param ResourceCommandContext context: the context object containing resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str mode: Snapshot save mode, can be one of two values 'shallow' (default) or 'deep'
        :param str custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        :rtype: OrchestrationSaveResult
        """

        # See below an example implementation, here we use jsonpickle for serialization,
        # to use this sample, you'll need to add jsonpickle to your requirements.txt file
        # The JSON schema is defined at:
        # https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        # You can find more information and examples examples in the spec document at
        # https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md
        '''
        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.

        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('REPLACE_WITH_ARTIFACT_TYPE', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
            saved_artifact=orchestration_saved_artifact)

        return OrchestrationSaveResult(saved_artifacts_info)
        '''
        pass

    def orchestration_restore(self, context, cancellation_context, saved_artifact_info, custom_params):
        """
        Restores a saved artifact previously saved by this Shell driver using the orchestration_save function
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str saved_artifact_info: A JSON string representing the state to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        :return: None
        """
        '''
        # The saved_details JSON will be defined according to the JSON Schema and is the same object returned via the
        # orchestration save function.
        # Example input:
        # {
        #     "saved_artifact": {
        #      "artifact_type": "REPLACE_WITH_ARTIFACT_TYPE",
        #      "identifier": "16_08_09 11_21_35_657000"
        #     },
        #     "resource_name": "some_resource",
        #     "restore_rules": {
        #      "requires_same_resource": true
        #     },
        #     "created_date": "2016-08-09T11:21:35.657000"
        #    }

        # The example code below just parses and prints the saved artifact identifier
        saved_details_object = json.loads(saved_details)
        return saved_details_object[u'saved_artifact'][u'identifier']
        '''
        pass


    def show_power_state(self, context):
        response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/' % self.idrac_ip, verify=False,
                                auth=(self.idrac_username, self.idrac_password))
        data = response.json()
        tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
        msg = "%s power found %s at %s" % (self.resourcename, data[u'PowerState'], tstamp)
        self.logger.info(msg)
        csapi = CloudShellAPISession(host=context.connectivity.server_address,
                             token_id=context.connectivity.admin_auth_token,
                             username=None,
                             password=None,
                             domain=CloudShellSessionContext._get_domain(context))
        csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
        msg = "Power found %s at %s" % (data[u'PowerState'], tstamp)
        if data[u'PowerState'] == "On":
            csapi.SetResourceLiveStatus(self.resourcename,'Power ON',msg)
        else:
            csapi.SetResourceLiveStatus(self.resourcename,'Power OFF', msg)


    def power_on(self, context):
        tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
        csapi = CloudShellAPISession(host=context.connectivity.server_address,
                                     token_id=context.connectivity.admin_auth_token,
                                     username=None,
                                     password=None,
                                     domain=CloudShellSessionContext._get_domain(context))
        url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset' % self.idrac_ip
        payload = {'ResetType': 'On'}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,
                                 auth=('root', 'calvin'))
        statusCode = response.status_code
        if statusCode == 204:
            msg = "%s powering ON" % self.resourcename
            self.logger.info(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
            msg = "Powered ON at %s" % (tstamp)
            csapi.SetResourceLiveStatus(self.resourcename, 'Power ON', msg)
        else:
            msg = "%s - failed to power ON server, status code: %s,  %s" % \
                  (self.resourcename, statusCode, str(response.json()))
            self.logger.error(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
            msg = "Failed to power on at %s (timestamp)"
            csapi.SetResourceLiveStatus(self.resourcename, 'Error', msg)

    def power_off(self, context):
        tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
        csapi = CloudShellAPISession(host=context.connectivity.server_address,
                                     token_id=context.connectivity.admin_auth_token,
                                     username=None,
                                     password=None,
                                     domain=CloudShellSessionContext._get_domain(context))
        url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset' % self.idrac_ip
        payload = {'ResetType': 'ForceOff'}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,
                                 auth=(self.idrac_username, self.idrac_password))
        statusCode = response.status_code
        if statusCode == 204:
            msg = "%s powering OFF for reboot" % self.resourcename
            self.logger.info(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
            msg = "Powering OFF for reboot at %s" % (tstamp)
            csapi.SetResourceLiveStatus(self.resourcename, 'Power OFF', msg)
        else:
            msg = "%s - failed to power OFF server, status code: %s,  %s" % \
                  (self.resourcename, statusCode, str(response.json()))
            self.logger.error(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
            msg = "Failed to power OFF at %s" % (tstamp)
            csapi.SetResourceLiveStatus(self.resourcename, 'Error', msg)
            sys.exit()


    def ping_check(self, context):
        try:
            csapi = CloudShellAPISession(host=context.connectivity.server_address,
                                         token_id=context.connectivity.admin_auth_token,
                                         username=None,
                                         password=None,
                                         domain=CloudShellSessionContext._get_domain(context))
            ping_ret_code = subprocess.call(['ping', '-n', '2', self.resourceaddress], stdout=open(os.devnull, 'w'),
                                        stderr=open(os.devnull, 'w'))
            tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
            if ping_ret_code == 0:
                msg = "%s ping successful" % self.resourcename
                msg1 = "Ping successful at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Ping OK', msg1)
            else:
                msg = "%s did not answer ping. Still booting?" % (self.resourcename)
                msg1 = "Ping unsuccessful at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Info', msg1)
            self.logger.info(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
        except Exception as ex:
            msg = "Ping call failed, %s" % str(ex)
            self.logger.error(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
            msg = "Ping call failed at %s" % (tstamp)
            csapi.SetResourceLiveStatus(self.resourcename, 'Error', msg)

    ### Function to get current next boot onetime boot setting possible values for onetime boot
    def get_next_boot_current_setting(self, context):
        """
        :param ResourceCommandContext context: gg
        """
        csapi = CloudShellAPISession(host=context.connectivity.server_address,
                                     token_id=context.connectivity.admin_auth_token,
                                     username=None,
                                     password=None,
                                     domain=CloudShellSessionContext._get_domain(context))
        response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/' % self.idrac_ip, verify=False,
                                auth=(self.idrac_username, self.idrac_password))
        data = response.json()
        #print("\n-Supported values for next server reboot, one time boot:\n")
        #for i in data[u'Boot'][u'BootSourceOverrideTarget@Redfish.AllowableValues']:
        #    print(i)
        msg = "%s next reboot, one time setting: %s" % (self.resourcename, data[u'Boot'][u'BootSourceOverrideTarget'])
        self.logger.info(msg)
        csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)


    ### Function to set next boot onetime boot device.  Hard coded as Pxe option for now.
    def set_pxe_onetime_boot_device(self, context):
        csapi = CloudShellAPISession(host=context.connectivity.server_address,
                                     token_id=context.connectivity.admin_auth_token,
                                     username=None,
                                     password=None,
                                     domain=CloudShellSessionContext._get_domain(context))
        url = 'https://%s/redfish/v1/Systems/System.Embedded.1' % self.idrac_ip
        payload = {"Boot": {"BootSourceOverrideTarget": "Pxe"}}
        headers = {'content-type': 'application/json'}
        response = requests.patch(url, data=json.dumps(payload), headers=headers, verify=False,
                                auth=(self.idrac_username, self.idrac_password))
        data = response.json()
        statusCode = response.status_code
        if statusCode == 200:
            msg = "%s set next boot onetime boot device to: Pxe" % self.resourcename
            self.logger.info(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
            csapi.SetResourceLiveStatus(self.resourcename, 'PXE Set', 'Set to PXE boot')
        else:
            detail_message = str(response.__dict__)
            msg = "%s set boot command failed, errror code is %s,  %s" % (self.resourcename, statusCode, detail_message)
            self.logger.info(msg)
            csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)


    ### Function to reboot the server
    def reboot_server(self, context):
        csapi = CloudShellAPISession(host=context.connectivity.server_address,
                                     token_id=context.connectivity.admin_auth_token,
                                     username=None,
                                     password=None,
                                     domain=CloudShellSessionContext._get_domain(context))
        response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/' % self.idrac_ip, verify=False,
                                auth=(self.idrac_username, self.idrac_password))
        data = response.json()
        #print("\n- WARNING, Current server power state is: %s" % data[u'PowerState'])
        if data[u'PowerState'] == "On":
            url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset' % self.idrac_ip
            payload = {'ResetType': 'ForceOff'}
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,
                                    auth=(self.idrac_username, self.idrac_password))
            statusCode = response.status_code
            tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
            if statusCode == 204:
                msg = "%s powering OFF for reboot" % self.resourcename
                self.logger.info(msg)
                csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
                msg = "Powering OFF for reboot at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Progress 50', msg)
            else:
                msg = "%s - failed to power OFF (reboot), status code: %s,  %s" % \
                      (self.resourcename, statusCode, str(response.json()))
                self.logger.info(msg)
                csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
                csapi.SetResourceLiveStatus(self.resourcename, 'Error', 'Failed to power off for reboot')
                sys.exit()
            payload = {'ResetType': 'On'}
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,
                                     auth=('root', 'calvin'))
            tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
            statusCode = response.status_code
            if statusCode == 204:
                msg = "%s powered ON (reboot)" % self.resourcename
                self.logger.info(msg)
                csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
                msg = "Powered ON (reboot) at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Power ON', msg)
            else:
                msg = "%s - failed to power ON server, status code: %s,  %s" % \
                      (self.resourcename, statusCode, str(response.json()))
                self.logger.info(msg)
                csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
                msg = "Failed to power ON at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Error', msg)
                sys.exit()
        else:
            url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset' % self.idrac_ip
            payload = {'ResetType': 'On'}
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,
                                     auth=('root', 'calvin'))
            tstamp = datetime.datetime.now().strftime("%I:%M%p") + " UTC"
            statusCode = response.status_code
            if statusCode == 204:
                msg = "%s powered ON (reboot)" % self.resourcename
                self.logger.info(msg)
                csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
                msg = "Powered ON at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Power ON', msg)
            else:
                msg = "%s - failed to power ON, status code: %s,  %s" % \
                      (self.resourcename, statusCode, str(response.json()))
                self.logger.info(msg)
                csapi.WriteMessageToReservationOutput(context.reservation.reservation_id, msg)
                msg = "Failed to power ON at %s" % (tstamp)
                csapi.SetResourceLiveStatus(self.resourcename, 'Error', msg)


                # </editor-fold>
