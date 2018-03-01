# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:41:36 2018

@author: zli34
"""
import math
import numpy as np
import random
from Coalition import Coalition
from agent_cma_zl import Agent
#from environ_config import environ as environ

class Coalition_Crime(Coalition):
    """A subclass of Coalition
    Attributes:
        of_type: The type of the coalition
        members: List of agents in the coalition
        uid: unique ID for coalition
        network: The original network id where the coalition is nested in 
        resources: The amount of each asset the coalition has
        history_self, history_others: The coalition's memory of history of itself and others
        policy: The coalition's policy
        competitors: The coalition's competitors
        
        location
        combined_crime_propensity
    """
    def __init__(self, of_type = None, members = [], resources = [], uid = None, network = None, history_self = [], history_others = [], policy=None, competitors = [], x=0, y=0, combined_crime_propensity=0):
        Coalition.__init__(self, of_type = of_type, members=members, resources=resources, uid =uid, network=network,
                           history_self=history_self, history_others=history_others, policy=policy, competitors=competitors)
        self.x = x
        self.y = y
        self.combined_crime_propensity = combined_crime_propensity
    
    def move_together(self, width, height):
        while True:
            d = random.sample([1,2,3,4],1)[0]
            if d == 1 and self.x-1 >= 0:
                self.x = self.x-1
                for i in self.members:
                    i.x = i.x-1
                break
            if d == 2 and self.y-1 >= 0:
                self.y = self.y-1
                for i in self.members:
                    i.y = i.y-1
                break
            if d == 3 and self.x+1 <= width:
                self.x = self.x+1
                for i in self.members:
                    i.x = i.x+1
                break
            if d == 4 and self.y+1 <= height:
                self.y = self.y+1
                for i in self.members:
                    i.y = i.y+1
                break
        
        
    def merge_with_coalition(self, other_coalition):
        if self.can_merge_with_coalition(self, other_coalition):
            for member in other_coalition.members:
                self.members.append(member)
                self.combined_crime_propensity += 1
            del other_coalition
        
        
    def can_merge_with_coalition(self, other_coalition):
        return self.crime_propensity < self.network.threshold_propensity and other_coalition.crime_propensity < network.threshold_propensity
    
    def commit_crime(self, civilians, police, threshold, radius):
        victims = self.can_commit_crime(cell_radius=radius, threshold=threshold, civilians=civilians, police=police)
        if victims:
            #of_type = 1 means civilian
            #Agent.cell_radius needs to be modified
            victims = self.members[0].look_for_agents(agent_role = Agent.Role.CIVILIAN, cell_radius = radius )
            #victim = victims 

            victim = random.choice(victims)
            victim.resources[0] = 0.5*victim.resources[0]
            
            #history_others means a civilian's memory
            victim.history_others = victim.history_others + self.members
            #remove the same elements in memory
            #victim.memory=[set(victim.memory)]
            
            for member in self.members:
                member.resources[0] += victim.resources[0] / len(self.members)
                member.crime_propensity += 1
                self.combined_crime_propensity += 1   
            
            return True
                
    def can_commit_crime(self, cell_radius, threshold, civilians, police):
        # FIXME Temporary fix to ensure propensity is updated - remove later for efficiency's sake
        self.update_propensity()
        if self.combined_crime_propensity < threshold:
            return False
        
        #of_type = 1 means civilian
        #Agent.cell_radius needs to be modified
        if len(self.members[0].look_for_agents(agent_role=Agent.Role.CIVILIAN, cell_radius = cell_radius)) == 0:
            return False
        
        #of_type = 2 means police
        if len(self.members[0].look_for_agents(agent_role=Agent.Role.POLICE, cell_radius = cell_radius)) > 0:
            return False
        
        return True
        
    def update_propensity(self):
        """
        Helper class to update the combined_propensity variable
        :return: void
        """

        if len(self.members) == 0:
            self.combined_crime_propensity = 0

        else:
            self.combined_crime_propensity = 0
            for member in self.members:
                self.combined_crime_propensity += member.crime_propensity
